from utils.helpers import get_config, write_config, get_external_ip, get_port, get_masternode_key, ensure_config_exists

ensure_config_exists()
conf=get_config()
ip=get_external_ip()

conf['listen'] = 1
conf['logtimestamps'] = 1
conf['maxconnections'] = 256
conf['port'] = get_port()
conf['masternode'] = 1
conf['externalip'] = ip
conf['bind'] = ip
conf['masternodeaddr'] = "%s:%s" % (ip, get_port())
conf['masternodeprivkey'] = get_masternode_key()

write_config(conf)
