## Ryousei's Sandbox: small utilities and etc for ABCI

### Preparation
- Requirement: OpenSSH (7.3 or later)

- Add ProxyJump setting in $HOME/.ssh/config as follows. Note: you should replace ```abciuser``` with your user account.

- ```
  Host abci:
      HostName es
      User abciuser
      ProxyJump %r@as.abci.ai
  ```

* FYI: See https://gist.github.com/ogawa/1d61d0241b82af802d99cba7cb03d1ff

### Well known problems

* This script works on macOS only, because it uses ```open``` command.