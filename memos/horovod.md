## Horovod

### Getting started on ABCI

1. Install Horovod on venv environment.

   ```shell
   $ python3 -m venv horovod
   $ source horovod/bin/activate
   
   $ module load python/3.6/3.6.5
   $ module load openmpi/2.1.5
   $ module load cuda/9.0/9.0.176.4
   $ module load cudnn/7.1/7.1.4
   $ module load nccl/2.3/2.3.7-1
   $ pip install --upgrade pip
   $ pip install keras tensorflow-gpu
   $ pip install horovod
   ```

   * Note: openmpi/3.x module does not currently support CUDA.

2. Run an example script on a machine with 4 GPUs.

   * Job script

     ```bash
     #!/bin/bash
     
     #$-l rt_F=1
     #$-j y
     #$-cwd
     
     source /etc/profile.d/modules.sh
     module load python/3.6/3.6.5
     module load openmpi/2.1.5
     module load cuda/9.0/9.0.176.4
     module load cudnn/7.1/7.1.4
     module load nccl/2.3/2.3.7-1
     
     source horovod/bin/activate
     
     mpirun -np 4 \
         -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH -x PATH \
         -mca pml ob1 -mca btl ^openib \
         python sw/horovod/examples/keras_mnist.py
     ```

   * Submit the job script

      ```bash
      $ qsub -g XXXXXXXX keras_mnist.sh
      Your job 123456 ("keras_mnist.sh") has been submitted
      
      $ tail -F keras_mnist.sh.o123456
      :
      ```

3. Run an example script on 2 machines with 4 GPUs each.

   * Job script

     ```bash
     #!/bin/bash
     
     #$-l rt_F=2
     #$-j y
     #$-cwd
     
     source /etc/profile.d/modules.sh
     module load python/3.6/3.6.5
     module load openmpi/2.1.5
     module load cuda/9.0/9.0.176.4
     module load cudnn/7.1/7.1.4
     module load nccl/2.3/2.3.7-1
     
     source horovod/bin/activate
     
     mpirun -np 8 -npernode 4 \
         -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH -x PATH \
         -mca pml ob1 -mca btl openib \
         python sw/horovod/examples/keras_mnist.py
     ```

### Benchmark

1. Clone the benchmark script. Note: we should use a branch corresponding to the version of TensorFlow.

   ```bash
   $ git clone https://github.com/tensorflow/benchmarks
   $ cd benchmarks
   $ git fetch
   $ git checkout -b cnn_tf_v1.12_compatible origin/cnn_tf_v1.12_compatible
   $ git branch
   * cnn_tf_v1.12_compatible
     master
   ```

2. Run the benchmark.

### References

* https://github.com/uber/horovod

