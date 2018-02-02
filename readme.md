# masternode helper scripts

original source: https://denariustalk.org/index.php?/topic/129-dnr-masternode-setup

## initial security setup

if you already have a secure box and a user, just skip right now down to section "masternode setup"

### 1 change your root password

```sh
passwd root
```

### 2 install scripts and some deps

```sh
apt-get update
apt-get upgrade
apt-get install ufw python virtualenv git unzip pv make
git clone https://github.com/pyramation/mn-setup-scripts.git
cd mn-setup-scripts && ./install.sh
```

### 3 add user

make sure `/root/.ssh/authorized_keys` exists first! If you used DigitalOcean or similar, should already be there ;)

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


### 0 install denarius

Log back in, then switch to root (or can use sudo):

```
su - root
apt-get install build-essential libssl-dev libdb++-dev libboost-all-dev libminiupnpc-dev libqrencode-dev
```

then type `exit` if root, to go back to regular user:

```
cd ~/
git clone https://github.com/carsenk/denarius
cd denarius
git checkout masternodes # CAREFUL THIS STEP MAY BE DIFFERENT WHEN IN PRODUCTION!
cd src
make -f makefile.unix
```

### 1 setup env vars

navigate to `denarius/src` where `./denariusd` lives, and setup env vars:
[comment]: <> (TODO: maybe should just use raw_input to ask user these variables...)

```sh
cd ~/denarius/src
export MN_ALIAS=pyramation
export TESTNET=1
```

### 2 generate the config

```sh
mkdir -p ~/.denarius
mn-setup-init-config
```

### 3 start `denariusd`

```sh
cd ~/denarius/src
./denariusd
```

### 4 load up on 5000 coin!

Now, open another shell, and navigate to the `src/` dir

```sh
cd ~/denarius/src
./denariusd getaccountaddress 0
>> 8aEgCZRJcmSUymnd8mLsQqE9SfWAnGYZrB
```

Send 5000 DNR to that address

### 5 update `denarius.conf` with masternode info

```sh
cd ~/denarius/src
mn-setup-update-config
```

### 6 generate `masternode.conf`

First, wait until you are sync'd and have coins!

```sh
cd ~/denarius/src
./denariusd getbalance
>> 5000.00
```

When ready, generate the config:

```sh
cd ~/denarius/src
mn-setup-init-masternode-config
```

### 7 restart `denariusd`

In one shell,

```sh
./denariusd stop
```

then in the original one running `./denariusd`, hit `ctl+c`, then

```sh
./denariusd
```

### 8 start your masternode

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

### clean your history!

As an extra security precaution, in case you entered a passphrase or other sensitive information via the command line, this line will completely erase all of your bash history:

```sh
cat /dev/null > ~/.bash_history && history -c
```

### get the alias name

```sh
cat ~/.denarius/masternode.conf
```

### if you encrypted your wallet

you may to to use `walletpassphrase` to start the alias, so far this order works:

```sh
./denariusd masternode start-alias <aliasname>
./denariusd walletpassphrase <passphrase> 10000000
./denariusd masternode start
./denariusd masternode debug
```
