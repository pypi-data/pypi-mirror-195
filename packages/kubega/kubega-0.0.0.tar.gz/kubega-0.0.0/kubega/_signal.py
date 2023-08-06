"""
Processing SIGINT and SIGTERM gracefully.
"""
import logging
import signal

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def get_exit_flag():
    return EXIT_FLAG


def _handler(signum, frame):
    global EXIT_FLAG
    EXIT_FLAG = True
    LOG.debug("Got signal {}...".format(signum))
    if signum == signal.SIGINT:
        LOG.info("Got SIGINT, exiting gracefully... "
                 "Send signal again to force exit.")
        signal.signal(signal.SIGINT, SIGINT_HANDLER)


EXIT_FLAG = False
SIGINT_HANDLER = signal.getsignal(signal.SIGINT)
signal.signal(signal.SIGTERM, _handler)
signal.signal(signal.SIGINT, _handler)
