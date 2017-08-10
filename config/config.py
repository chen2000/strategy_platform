from __future__ import absolute_import

import yaml
import os


path = os.path.dirname(__file__)
with open(path + "/settings.yaml", 'r') as f:
    settings = yaml.load(f)
