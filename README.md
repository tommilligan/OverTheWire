# OverTheWire

Working notes and utilities for http://overthewire.org/


## `otw`

### Brief

`otw` is an automatic connection and password helper for OverTheWire.
It can be used to remember your flags and connect automatically to wargames.


### Installation

`otw` uses `sshpass` to automate `ssh` initiation. Install using your distro's package manager, and make sure it can be found on the `PATH`.

```bash
sudo dnf install sshpass
```

After, just clone the repo to wherever you want it.


### Use

To connect a new level, provide the password with the `-p` flag.

```bash
./otw bandit 0 -p bandit0
```

Once the password has been given, it will automatically be recalled.

```bash
./otw natas 5
```

Calling a level with the `-p` flag again will overwrite the old password.

To add new wargame connection details, simply add them to `connections.yml`.

