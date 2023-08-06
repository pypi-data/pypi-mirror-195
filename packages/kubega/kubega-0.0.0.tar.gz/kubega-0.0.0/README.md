## kubega-core

Learning the code of Pollux [OSDI '21], renamed as kubeGA.

kubeGA implements a lightweight checkpointing and a collective communication tool. 
kubega-core is the core lib of kubega.

The main algorithmic part of kubeGA is the fitting of goodput function. However, to use 
it, we have to integrate the dynamic batch size and learning rate adjusting into the data parallel torch framework.
This is the engineering stuff.

This repo is opened only for study usage.
