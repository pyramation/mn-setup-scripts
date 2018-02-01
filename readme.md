# masternode helper scripts

original source: https://denariustalk.org/index.php?/topic/129-dnr-masternode-setup

# install

```sh
git clone https://github.com/pyramation/mn-setup-scripts.git
cd mn-setup-scripts && ./install.sh
source ~/.profile
```






# TODO

- [x] add a flag for testnet
- [x] move variables to env variables
- [ ] double check assumptions w dnr devs
- [ ] add better documention
- [ ] try doing walletpassphrase before start-alias and see if it works

# setup

### go to src folder

navigate to `denarius/src` where `./denariusd` lives, for now you can just run these python files from there.

### setup env vars

```sh
export MN_ALIAS=pyramation
export TESTNET=1
```

### generate the config

```sh
mn-setup-init-config
```

### start `denariusd`

```sh
./denariusd
```

### update `denarius.conf` with masternode info

```sh
mn-setup-update-config
```

### generate `masternode.conf`

```sh
mn-setup-init-masternode-config
```

### restart `denariusd`

In one shell,

```sh
./denariusd stop
```

then in the original one running `./denariusd`, hit `ctl+c`, then

```sh
./denariusd
```

### start your masternode

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
