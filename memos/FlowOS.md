## FlowOS Job

### Getting started on ABCI

Note: You should read the FlowOS document in details.

1. Install FlowOS Job on venv environment.

   ```shell
   $ module load python/3.6/3.6.5
   $ python3 -m venv flowos
   $ source flowos/bin/activate

   $ module load cuda/9.2/9.2.88.1
   $ pip3 install cython numpy

   $ git clone XXX
   $ cd flowos-job
   $ python3 setup.py install
   ```

2. Run MNIST training example

   Chainer is required to load a pre-learned model.

   ```shell
   $ pip3 install chainer tqdm
   $ pip3 freeze
   chainer==5.2.0
   Cython==0.29.5
   filelock==3.0.10
   flowos-job==0.2
   numpy==1.16.1
   protobuf==3.6.1
   six==1.12.0
   tqdm==4.31.1
   $ cd examples/train_mnist/
   $ python3 setup.py build_ext -i
   $ python3 ./train_mnist.py
   ```



### TODO

* How to install OpenCL on ABCI

