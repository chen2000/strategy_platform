from __future__ import absolute_import

import os
import errno

from config.config import settings


def make_input_file(index):
    return  os.path.join(
                settings['folder']['symbol'], 
                settings['symbol'][index] + '.csv'
            )

def make_output_file(index, frequency):
    out_dir = settings['folder']['trading']
    out_file = settings['trading'][frequency][index] + '.csv'
    try:
        os.makedirs(out_dir)
    except OSError as error:
        if error.errno != errno.EEXIST:	# errno is used to identify more granular error
            raise OSError
    return os.path.join(out_dir, out_file)
