## An automation script launching JupyterLab on ABCI

### Usage

```shell
$ python3 launch.py --help
usage: launch.py [-h] [-c CONFIG] [-m MODE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        specify an alternative config file (default:
                        config.ini)
  -m MODE, --mode MODE  specify a running mode: Singularity|Baremetal
                        (default: Singularity)
```



### Well known problems

- This script works on macOS only, because it uses ```open``` command.



### How to build a singularity image on macOS

- Vagrant (VirtualBox)

  - See https://singularity.lbl.gov/install-mac

- Docker

  - See https://github.com/kaczmarj/singularity-in-docker

    ```shell
    $ docker run --rm --privileged -v $(pwd):/work kaczmarj/singularity:2.6.1 \
      build ubuntu16.04.simg ubuntu16.04.recipe
    ```



### Notes on Singularity

- The --nv option is required when you use NVIDIA GPUs on a container as follows:

  ```shell
  $ singularity run --nv ubuntu16.04.simg
  ```



### Examples of Singularity recipe

- ubuntu16.04.recipe: CUDA 9.0, cuDNN 7.1.4, TensorFlow 1.2
- ubuntu18.04.recipe: CUDA 9.1, Chainer
  - Memo: TensorFlow (the official package of ubuntu 18.04; tensorflow-gpu) cannot work with CUDA 9.1.

