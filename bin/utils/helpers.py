# -*- coding: utf-8 -*-
from __future__ import absolute_import

import subprocess
import os.path
import json
import codecs
import os
import sys
import warnings
import re
from collections import OrderedDict

if 'MN_ALIAS' in os.environ:
    ALIAS=os.environ['MN_ALIAS']
else:
    ALIAS='denarius'

if 'TESTNET' in os.environ:
    TESTNET=os.environ['TESTNET']
else:
    print 'WARNING, USING MAINNET. Set the TESTNET env var to use testnet'
    TESTNET=0

if 'MN_PORT' in os.environ:
    PORT=os.environ['MN_PORT']
else:
    PORT=19999

if 'DATADIR' in os.environ:
    DATADIR=os.environ['DATADIR']
else:
    DATADIR='%s/.denarius' % os.environ['HOME']

DAEMON_PATH='./denariusd' # TODO assumes you are running from the src dir, please change
MASTERCONF='%s/masternode.conf' % DATADIR
DCONF='%s/denarius.conf' % DATADIR

__escape_decoder = codecs.getdecoder('unicode_escape')
__posix_variable = re.compile('\$\{[^\}]*\}')

def get_daemon_path():
    return '/home/denarius/denarius/src/denariusd'

def get_linux_user():
    return os.environ['USER']

def get_config_path():
    return DCONF

def get_config():
    return OrderedDict(parse_config(get_config_path()))

def write_config(config):
    with open(get_config_path(), "w") as f:
        for k, v in config.items():
            line='%s=%s' % (k, v)
            f.write('%s\n' % line.strip())
    return True

def write_initd():
    config = get_mn_config()
    daemon_name='dnr'

    print (
    """
cd /etc/init.d
    """
    )


    daemon_initd = """
#! /bin/sh
# Provides:          {daemon_name}
# Required-Start:    $remote_fs $syslog

case "$1" in
  start)
    echo "Starting daemon"
    sudo -u {user} {daemon}
    ;;
  stop)
    echo "Stopping daemon"
    sudo -u {user} {daemon} stop
    ;;
  *)
    echo "Usage: /etc/init.d/{daemon_name} (start|stop)"
    exit 1
    ;;
esac

exit 0
""".format(daemon_name=daemon_name, daemon=get_daemon_path(), user=get_linux_user())

    masternode_initd = """
#! /bin/sh
# Provides:          masternode
# Required-Start:    $remote_fs $syslog {daemon_name}

case "$1" in
  start)
    echo "Starting masternode"
    sleep 10
    sudo -u {user} {daemon} masternode start
    ;;
  stop)
    echo "Stopping masternode"
    sudo -u {user} {daemon} masternode stop
    ;;
  *)
    echo "Usage: /etc/init.d/masternode (start|stop)"
    exit 1
    ;;
esac

exit 0
""".format(daemon_name=daemon_name, daemon=get_daemon_path(), user=get_linux_user())

    print ('/etc/init.d/%s' % daemon_name)
    print (daemon_initd)

    print ('/etc/init.d/masternode')
    print (masternode_initd)

    print (
    """
cd /etc/init.d
chmod 755 masternode
update-rc.d masternode defaults
chmod 755 {daemon_name}
update-rc.d {daemon_name} defaults
    """.format(daemon_name=daemon_name)
    )

    return True

def ensure_config_exists():
    conf = get_config_path()
    if not os.path.isfile(conf):
      raise Exception("%s is missing" % conf)

def ensure_config_does_not_exist():
    conf = get_config_path()
    if os.path.isfile(conf):
      raise Exception("%s already exists" % conf)

def use_testnet():
  return TESTNET

def get_port():
  return PORT

def get_mn_config_path():
    return MASTERCONF

def get_mn_config():
    return parse_mn_config(get_mn_config_path())

def write_mn_config(opts):
    conf=get_config()
    with open(get_mn_config_path(), "w") as f:
        f.write('%s %s:%s %s %s %s' % (opts['alias'].strip(), conf['externalip'], conf['port'], conf['masternodeprivkey'], opts['txhash'], opts['txindex']))
    return True

def parse_mn_config(config_path):
    config = OrderedDict();
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            els = line.split()
            config['alias'] = els[0]
            config['ipport'] = els[1]
            config['masternodeprivkey'] = els[2]
            config['txhash'] = els[3]
            config['txindex'] = els[4]
    return config

def ensure_mn_config_exists():
    conf = get_mn_config_path()
    if not os.path.isfile(conf):
        raise Exception("%s is missing" % conf)

def decode_escaped(escaped):
    return __escape_decoder(escaped)[0]

def parse_config(config_path):
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)

            # Remove any leading and trailing spaces in key, value
            k, v = k.strip(), v.strip().encode('unicode-escape').decode('ascii')

            if len(v) > 0:
                quoted = v[0] == v[-1] in ['"', "'"]

                if quoted:
                    v = decode_escaped(v[1:-1])

            yield k, v

def get_random_alias():
    return "%s%s" % (ALIAS, subprocess.check_output(["openssl", "rand", "-hex", "5"]))

def get_random_rpcpassword():
    return subprocess.check_output(["openssl", "rand", "-hex", "22"])

def get_random_rpcuser(name):
    return "%s-%s" % (name, subprocess.check_output(["openssl", "rand", "-hex", "5"]))

def get_external_ip():
    return subprocess.check_output(["dig", "+short", "myip.opendns.com", "@resolver1.opendns.com"]).strip()

def get_masternode_key():
    try:
      return subprocess.check_output([DAEMON_PATH, "masternode","genkey"])
    except subprocess.CalledProcessError as e:
      raise Exception( "cannot generate a masternode key" )

def get_masternode_outputs():
    try:
      return json.loads(subprocess.check_output([DAEMON_PATH, "masternode","outputs"]))
    except subprocess.CalledProcessError as e:
      raise Exception( "cannot generate a masternode outputs" )

