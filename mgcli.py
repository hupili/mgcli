#!/usr/bin/env python

import sys
from os import path
import docopt
import requests
import json
import pandas
import jinja2
from pprint import pprint

__version__ = '0.0.10'

DOC = '''
{0} version {1}

Usage:
    {0} config list
    {0} config get <key>
    {0} config set <key> <domain> <api_key> <from_address>
    {0} config del <key>
    {0} send <key> <to> <subject> [--html=<file>] [--text=<file>] [--attachment=<file>]
    {0} send_template <key> <subject> <template.html> <data.csv>
    {0} --help

Args:
    <key>     The key of configuration item

Options:
    --help                   Show this message
    --html=<file>            The file containing the HTML email body
    --text=<file>            The file containing the text email body
    --attachment=<file>      The file containing the text email attachment
'''.format(path.basename(__file__), __version__)


FN_CONFIG=path.expanduser('~/.mgclirc')


def load_config():
    try:
        return json.load(open(FN_CONFIG))
    except IOError:
        # No such file
        pprint("Warning: can not find ~/.mgclirc. Use config '{}'")
        return {}


def list_config():
    config = load_config()
    return {
            'configurations': config.keys()
            }


def get_config(key):
    config = load_config()
    return {
            key: config.get(key, None)
            }


def del_config(key):
    config = load_config()
    if key in config:
        del config[key]
    json.dump(config, open(FN_CONFIG, 'w'))
    return {
            'ret': 'saved',
            'config': config
            }


def set_config(key, domain, api_key, from_address):
    config = load_config()
    config[key] = {
            'domain': domain,
            'api_key': api_key,
            'from_address': from_address
            }
    json.dump(config, open(FN_CONFIG, 'w'))
    return {
            'ret': 'saved',
            'config': config
            }


def _limit_length(data, field, length):
    if field not in data:
        return
    else:
        if len(data[field]) <= length:
            return
        else:
            data[field] = data[field][:length] + '...'
            return


def _send(key, to, subject, html=None, text=None, attachment=None):
    config = get_config(key)[key]
    url = 'https://api.mailgun.net/v2/%s/messages' % config['domain']
    data = {
            'config': config,
            'from': config['from_address'],
            'to': to,
            'subject': subject
            }
    if html:
        data.update({
            'html': html
            })
    elif text:
        data.update({
            'text': text
            })
    else:
        pprint('Warning: No email body is defined. Will send null message.')
        data.update({
            'text': 'null body'
            })

    if attachment:
        files = [('attachment', open(attachment))]
    else:
        files = None

    re = requests.post(url,
            auth=('api', config['api_key']),
            files=files,
            data=data)

    _limit_length(data, 'text', 50)
    _limit_length(data, 'html', 50)

    return {
            'data': data,
            'result': re
            }


def send(key, to, subject, html=None, text=None, attachment=None):
    if html:
        return _send(key, to, subject, html=open(html).read(), text=None, attachment=None)
    elif text:
        return _send(key, to, subject, html=None, text=open(text).read(), attachment=None)
    else:
        return _send(key, to, subject, html=None, text=None, attachment=None)


def send_template(key, subject, fn_template, fn_data):
    subject_template = jinja2.Template(subject)
    body_template = jinja2.Template(open(fn_template).read())
    data = pandas.read_csv(fn_data)
    ret = []
    for i, row in data.iterrows():
        to = row['to']
        subject = subject_template.render(row)
        body = body_template.render(row)
        ret.append(_send(key, to, subject, html=body))
    return ret


def main():
    args = docopt.docopt(DOC)

    config = load_config()

    if args['config']:
        if args['list']:
            return list_config()
        elif args['get']:
            return get_config(args['<key>'])
        elif args['set']:
            return set_config(
                    args['<key>'],
                    args['<domain>'],
                    args['<api_key>'],
                    args['<from_address>'])
        elif args['del']:
            return del_config(args['<key>'])
        else:
            assert(False)
    elif args['send']:
        return send(
                args['<key>'],
                args['<to>'],
                args['<subject>'],
                args['--html'],
                args['--text'],
                args['--attachment']
                )
    elif args['send_template']:
        return send_template(
                args['<key>'],
                args['<subject>'],
                args['<template.html>'],
                args['<data.csv>']
                )
    else:
        assert(False)

if __name__ == '__main__':
    pprint(main())
