#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.dirname(__file__) + '/../datashack_infra_app')

import json
import os
import subprocess
import sys
from typing import Dict, List
from cdktf import App
from additional_plugins.datashack_glue import GlueTableConf
from additional_plugins import DatashackStack, DatashackStackConf
import json 
import re
import tempfile
import shutil


def create_app_with_resource(env_data: Dict):
    app = App()
    
    resources = env_data["resources"]

    stack_conf = DatashackStackConf(
        env=env_data['env_id'],
        resources=resources)

    DatashackStack(app, stack_conf)
    app.synth()


def _move_to_this_dir():
    # move to this folder as we need to be in cdktf context now
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


if __name__ == '__main__':
    inp = sys.argv[1]
    print('input is', inp)
    # fix a windows issue not removing the single qoute ...
    if inp[0] == "'":
        inp = inp[1:-1]
        print('trimmed input to', inp)

    env_data = json.loads(inp)
    create_app_with_resource(env_data)
