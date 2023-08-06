import math

from torchtext.data import BPTTIterator
from torchtext.data.batch import Batch
from torchtext.data.dataset import Dataset

from kubega import env
from kubega.torch.data import AdaptiveDataLoaderMixin


class AdaptiveBPTTIterator(BPTTIterator, AdaptiveDataLoaderMixin):
    """
    An adaptive DataLoader built for BPTT iterator. Used for test.
    """

    def __init__(self, dataset, batch_size, bptt_len, **kwargs):
        max_batch_size = kwargs.pop("max_batch_size", None)
        local_bsz_bounds = kwargs.pop("local_bsz_bounds", None)

        BPTTIterator.__init__(self, dataset=dataset, batch_size=batch_size,
                              bptt_len=bptt_len, **kwargs)
        AdaptiveDataLoaderMixin.__init__(self, batch_size)

        self.num_replicas = env.num_replicas()
        self.rank = env.replica_rank()

        if max_batch_size and local_bsz_bounds:
            self._elastic.autoscale_batch_size(max_batch_size,
                                               local_bsz_bounds)

    def __iter__(self):
        with self._elastic.context():
            if self._elastic.skipdone():
                return

            self.batch_size = self._elastic.sync_local_bsz()

            text = self.dataset[0].text
            text_field = self.dataset.fields['text']
            text_field.eos_token = None
            text = text + ([text_field.pad_token] *
                           int(math.ceil(len(text) / self.batch_size) *
                               self.batch_size - len(text)))
            data = text_field.numericalize(
                [text], device=self.device)
            data = data.view(self.batch_size, -1).t().contiguous()
            dataset = Dataset(examples=self.dataset.examples, fields=[
                ('text', text_field), ('target', text_field)])
            end = data.size(0)  # current length of dataset

            # Change in current batch size changes the dimensions of dataset
            # which changes the starting position in the reshaped dataset. The
            # local batch size is also a function of number of replicas, so
            # when we rescale we need to recalculate where to start the
            # iterations from for the new batch size.
            self._elastic.current_index = \
                _recompute_start(self._elastic.current_index,
                                 self._elastic.end_index, end)
            self._elastic.end_index = end

            # Every replica reads data strided by bptt_len
            start = self._elastic.current_index + (self.bptt_len * self.rank)
            step = self.bptt_len * self.num_replicas

            # The starting index of the highest rank
            highest_start = self._elastic.current_index + (self.bptt_len * (self.num_replicas - 1))

            # Number of steps we will take on the highest rank. We limit
            # iterations on all replicas by this number to prevent asymmetric
            # reduce ops which would result in a deadlock.
            min_steps_in_epoch = max(math.ceil((end - highest_start) / step), 0)  # noqa: E501
            self.iterations = 0
            while True:
                for i in range(start, end, step):
                    self.iterations += 1
                    # Make sure that _elastic.profile is called equal number of
                    # times on all replicas
                    if self.iterations > min_steps_in_epoch:
                        break
                    with self._elastic.profile(self.training and i > 0):
                        seq_len = min(self.bptt_len, data.size(0) - i - 1)
                        assert seq_len > 0
                        batch_text = data[i:i + seq_len]
                        batch_target = data[i + 1:i + 1 + seq_len]
                        if text_field.batch_first:
                            batch_text = batch_text.t().contiguous()
                            batch_target = batch_target.t().contiguous()
                        yield Batch.fromvars(
                            dataset, self.batch_size,
                            text=batch_text,
                            target=batch_target)
                        self._elastic.current_index += step

                if not self.repeat:
                    break


def _recompute_start(prev_cur, prev_end, cur_end):
    # The start index changes when there is a rescaling. We recompute a new
    # start index based on how much we covered before the restart.
    if prev_end == 0:
        return prev_cur
    return math.ceil(prev_cur * cur_end / prev_end)
