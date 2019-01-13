import argparse
import configparser
from pathlib import Path
import pexpect
import subprocess
import sys
from time import sleep

CONFIG_FILE = "config.ini"
PROMPT = r"\[\w+@\w+ \S+\].*"

QRSH_CMD = "qrsh -g {} -l {}"
JUPYTER_URI = "http://\(([\w]+\.abci\.local) or 127\.0\.0\.1\):{}/\?token=(\w+)"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify an alternative config file (default: config.ini)", default=CONFIG_FILE)
    parser.add_argument("-m", "--mode", help="specify a running mode: Singularity|Baremetal (default: Singularity)", default="Singularity")
    args = parser.parse_args()

    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    if Path(args.config).exists():
        config.read(args.config)
    else:
        print("No such file: {}.".format(args.config))
        sys.exit(1)

    print("Connecting ABCI...")
    conn = pexpect.spawn('ssh abci') # you have to edit .ssh/config for ProxyJump.

    print("Submitting an interactive job...")
    conn.sendline(QRSH_CMD.format(config['Common']['group'], config['Common']['resource']))
    conn.expect(PROMPT)

    print("Launching Jupyter Lab:...")
    for cmd in config[args.mode]['prologue'].splitlines():
        if cmd != '':
            print("    {}".format(cmd))
            conn.sendline(cmd)
            conn.expect(PROMPT)

    cmd = config[args.mode]['main']
    print("    {}".format(cmd))
    conn.sendline(cmd)
    conn.expect(JUPYTER_URI.format(config['Common']['port']))
    node = conn.match.group(1).decode('utf-8')
    token = conn.match.group(2).decode('utf-8')

    print("Setting up an SSH tunnel...")
    proc = subprocess.Popen(["ssh", "-N", "-L", "{}:{}:{}".format(config['Common']['local_port'], node, config['Common']['port']), "abci"])
    sleep(1)

    print("Launching a web browser...")
    subprocess.call(["open", "http://127.0.0.1:{}/?token={}".format(config['Common']['local_port'], token)])

    print("Jupyter Lab is running...")
    while True:
        try:
            # Wait until this jupytrlab is shutdown.
            #conn.interact()
            conn.expect(PROMPT)
            break
        except pexpect.EOF:
            break
        except pexpect.TIMEOUT:
            pass
        except KeyboardInterrupt:
            break

    print("Terminating...")
    proc.terminate()
    sleep(1)
