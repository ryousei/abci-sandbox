import argparse
import configparser
from pathlib import Path
import sys
import subprocess
import pexpect
from time import sleep

CONFIG_FILE = "config.ini"
PROMPT = r"\[\w+@\w+ \S+\].*"

QRSH_CMD = "qrsh -g {} -l {}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify an alternative config file (default: config.ini)", default=CONFIG_FILE)
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

    print("Launching VNC server...")
    conn.sendline("vncserver")
    conn.expect("desktop is ([\w]+\.abci\.local):(\d+)")
    node = conn.match.group(1).decode('utf-8')
    session = conn.match.group(2).decode('utf-8')
    port = int(config['Common']['port']) + int(session)
    local_port = int(config['Common']['local_port']) + int(session)
    conn.expect(PROMPT)


    print("Setting up an SSH tunnel...")
    proc = subprocess.Popen(["ssh", "-N", "-L", "{}:{}:{}".format(local_port, node, port), "abci"])
    sleep(1)

    print("Launching a VNC client...")
    subprocess.call(["open", "vnc://127.0.0.1:{}/".format(local_port)])

    print("NOTE: don't forget to terminate vncserver. Run \"vncserver -kill :{}\" before logout this session.".format(session))
    while True:
        try:
            conn.interact()
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
