## An automation script launching VNC server & client (remote desktop)

### Usage

```shell
$ python3 launch.py --help
usage: launch.py [-h] [-c CONFIG] [-m MODE]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        specify an alternative config file (default:
                        config.ini)
```

### Well known problems

- This script works on macOS only, because it uses ```open``` command.

