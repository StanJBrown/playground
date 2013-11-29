#!/usr/bin/env python
import json

def load_config(config_file):
    config = json.loads(open(config_file).read())
    return config
