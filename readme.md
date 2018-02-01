# masternode helper scripts

original source: https://denariustalk.org/index.php?/topic/129-dnr-masternode-setup

## initial security setup

if you already have a secure box and a user, just skip right now down to section "masternode setup"

### 1 install scripts and some deps

```sh
git clone https://github.com/pyramation/mn-setup-scripts.git
cd mn-setup-scripts && ./install.sh
source ~/.profile
apt-get update
apt-get upgrade
apt-get install ufw python virtualenv git unzip pv make
```

### 2 change your root password

```sh
passwd root
```

### 3 add user

```sh
mn-setup-init-user <username>
```

Write down the username it creates! Added randomness for extra security.

### 4 add firewalls

```sh
mn-setup-firewalls
reboot
```

# masternode setup


### 1 setup env vars

navigate to `denarius/src` where `./denariusd` lives, and setup env vars:

```sh
export MN_ALIAS=pyramation
export TESTNET=1
```

### 2 generate the config

```sh
mn-setup-init-config
```

### 3 start `denariusd`

```sh
./denariusd
```

### 4 update `denarius.conf` with masternode info

```sh
mn-setup-update-config
```

### 5 generate `masternode.conf`

```sh
mn-setup-init-masternode-config
```

### 6 restart `denariusd`

In one shell,

```sh
./denariusd stop
```

then in the original one running `./denariusd`, hit `ctl+c`, then

```sh
./denariusd
```

### 7 start your masternode

look at the alias inside of `masternode.conf`

```sh
 ./denariusd masternode start-alias <your alias>
```

To ensure the masternode is running properly you can use the debug command:

```sh
./denariusd masternode debug
```

If the output says “ masternode is stopped ” then run the following command:

```sh
./denriusd masternode start
```


## notes

to get the alias name

```sh
cat ~/.denarius/masternode.conf
```

you may to to use `walletpassphrase` to start the alias, so far this order works:

```sh
./denariusd masternode start-alias <aliasname>
./denariusd walletpassphrase <passphrase> 10000000
./denariusd masternode start
./denariusd masternode debug
```
