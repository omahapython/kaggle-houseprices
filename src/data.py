#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
load_settings_json
"""

import json
import logging
import os
from collections import OrderedDict as odict
from os.path import dirname, join  # realpath

DEFAULT_SETTINGS = odict()
DEFAULT_SETTINGS['TRAIN_DATA_PATH'] = 'input/'
DEFAULT_SETTINGS['TEST_DATA_PATH'] = 'input/'
DEFAULT_SETTINGS['MODEL_PATH'] = 'working/'
DEFAULT_SETTINGS['SUBMISSION_PATH'] = 'working/'


def load_settings_json(filename='settings.json', settings_json_path=None):
    """load settings.json

    Keyword Arguments:
        filename (str): default: settings.json
        settings_json_path (str): full path to settings.json (overrides filename)

    Returns:
        OrderedDict: dict of settings

    Raises:
        OSError: (FileNotFoundError w/ Python 3) when the filename or path
            doesn't exist
        ValueError: when the JSON file is not valid JSON
            (try ``python -m json.tool <filename>``)
    """
    here = dirname(__file__)
    if settings_json_path is None:
        settings_json_path = join(here, '..', filename)
    log = logging.getLogger('data.py')
    log.info("PWD=%r" % os.environ['PWD'])
    log.info("Reading settings from %r"  % settings_json_path)
    with open(settings_json_path, 'r') as f:
        data = json.load(f, object_pairs_hook=odict)
    for key in DEFAULT_SETTINGS:
        if key not in data:
            data[key] = DEFAULT_SETTINGS[key]
    for key in DEFAULT_SETTINGS:
        data[key] = join(here, '..', data[key])
    return data


import unittest


class Test_load_settings_json(unittest.TestCase):

    def test_load_settings_json(self):
        cfg = load_settings_json()
        for key in DEFAULT_SETTINGS:
            self.assertTrue(key in cfg)
        # raise Exception(cfg)

    def test_load_settings_json_fail(self):
        with self.assertRaises(OSError):
            load_settings_json('SETTINGZ.json')

        with self.assertRaises(OSError):
            load_settings_json(settings_json_path='/settings..json')


def main(argv=None):
    """
    Main function

    Keyword Arguments:
        argv (list): commandline arguments (e.g. sys.argv[1:])
    Returns:
        int: zero
    """
    import logging
    import optparse

    prs = optparse.OptionParser(usage="%prog : args")

    prs.add_option('-f', '--filename',
                   dest='filename',
                   action='store',
                   default='settings.json')
    prs.add_option('--path',
                   dest='settings_json_path',
                   action='store')

    prs.add_option('-w', '--write-defaults',
                   dest='write_settings_json_defaults',
                   action='store')

    prs.add_option('-v', '--verbose',
                   dest='verbose',
                   action='store_true',)
    prs.add_option('-q', '--quiet',
                   dest='quiet',
                   action='store_true',)
    prs.add_option('-t', '--test',
                   dest='run_tests',
                   action='store_true',)

    argv = list(argv) if argv else []
    (opts, args) = prs.parse_args(args=argv)
    loglevel = logging.INFO
    if opts.verbose:
        loglevel = logging.DEBUG
    elif opts.quiet:
        loglevel = logging.ERROR
    logging.basicConfig(level=loglevel)
    log = logging.getLogger()
    log.debug('argv: %r', argv)
    log.debug('opts: %r', opts)
    log.debug('args: %r', args)

    if opts.run_tests:
        import sys
        sys.argv = [sys.argv[0]] + args
        import unittest
        return unittest.main()

    if opts.write_settings_json_defaults:
        with open(opts.write_settings_json_defaults, 'w') as f:
            json.dump(DEFAULT_SETTINGS, f)
            log.info("Wrote DEFAULT_SETTINGS to %r"
                     % opts.write_settings_json_defaults)
        opts.settings_json_path = opts.write_settings_json_defaults

    EX_OK = 0
    output = load_settings_json(
        filename=opts.filename,
        settings_json_path=opts.settings_json_path)
    print(json.dumps(output, indent=2))
    return EX_OK


if __name__ == "__main__":
    import sys
    sys.exit(main(argv=sys.argv[1:]))
