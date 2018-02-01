#!/usr/bin/env python
from collections import OrderedDict
from utils.helpers import ensure_config_exists, write_mn_config, get_random_alias, get_masternode_outputs

ensure_config_exists()

outputs=get_masternode_outputs()
mconf=OrderedDict()
mconf['alias'] = get_random_alias()
mconf['txhash'] = next(iter(outputs))
mconf['txindex'] = outputs.values()[0]

write_mn_config(mconf)
