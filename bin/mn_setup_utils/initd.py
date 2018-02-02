# -*- coding: utf-8 -*-
from __future__ import absolute_import
import subprocess
import os

def generate_initd(daemon_name, daemon, user):
    return """#! /bin/sh
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
""".format(daemon_name=daemon_name, daemon=daemon, user=user)

def generate_masternode_initd(daemon_name, daemon, user):
    return """#! /bin/sh
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
""".format(daemon_name=daemon_name, daemon=daemon, user=user)

def write_initd_files(daemon_name, daemon, user):

    daemon_initd = generate_initd(daemon_name, daemon, user)
    masternode_initd = generate_masternode_initd(daemon_name, daemon, user)

    print (daemon_initd)
    print (masternode_initd)

    with open('/etc/init.d/%s' % daemon_name, "w") as f:
        f.write(daemon_initd)

    with open('/etc/init.d/masternode', "w") as f:
        f.write(masternode_initd)

    cwd = os.getcwd()
    os.chdir('/etc/init.d')
    subprocess.check_output(['chmod', '755', daemon_name])
    subprocess.check_output(['chmod', '755', 'masternode'])
    # order matters
    subprocess.check_output(['update-rc.d', daemon_name, 'defaults'])
    subprocess.check_output(['update-rc.d', 'masternode', 'defaults'])
    os.chdir(cwd)
