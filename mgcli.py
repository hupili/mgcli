#!/usr/bin/env python

import sys
from os import path
import docopt
import requests
import json
import pandas
import jinja2
from pprint import pprint

__version__ = '0.0.7'

DOC = '''
{0} version {1}

Usage:
    {0} config get
    {0} config set <domain> <api_key> <from_address>
    {0} send <to> <subject> [--html=<file>] [--text=<file>] [--attachment=<file>]
    {0} send_template <subject> <template.html> <data.csv>
    {0} --help

Options:
    --help                   Show this message
    --html=<file>            The file containing the HTML email body
    --text=<file>            The file containing the text email body
    --attachment=<file>      The file containing the text email attachment
'''.format(path.basename(__file__), __version__)


FN_CONFIG=path.expanduser('~/.mgclirc')


def load_config():
    return json.load(open(FN_CONFIG))


def save_config(domain, api_key, from_address):
    config = {
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
        if data[field] <= length:
            return
        else:
            data[field] = data[field][:length] + '...'
            return


def _send(to, subject, html=None, text=None, attachment=None):
    config = load_config()
    url = 'https://api.mailgun.net/v2/%s/messages' % config['domain']
    data={'from': config['from_address'],
            'to': to,
            'subject': subject}
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


def send(to, subject, html=None, text=None, attachment=None):
    if html:
        return _send(to, subject, html=open(html).read(), text=None, attachment=None)
    elif text:
        return _send(to, subject, html=None, text=open(text).read(), attachment=None)
    else:
        return _send(to, subject, html=None, text=None, attachment=None)


def send_template(subject, fn_template, fn_data):
    subject_template = jinja2.Template(subject)
    body_template = jinja2.Template(open(fn_template).read())
    data = pandas.read_csv(fn_data)
    ret = []
    for i, row in data.iterrows():
        to = row['to']
        subject = subject_template.render(row)
        body = body_template.render(row)
        ret.append(_send(to, subject, html=body))
    return ret


def main():
    args = docopt.docopt(DOC)

    try:
        config = load_config()
    except IOError:
        pprint('warning: can not find ~/.mgclirc, we have created one for you')
        save_config('domain', 'api_key', 'from_address')
        config = load_config()

    if args['config']:
        if args['get']:
            return load_config()
        elif args['set']:
            return save_config(args['<domain>'],
                    args['<api_key>'],
                    args['<from_address>'])
        else:
            assert(False)
    elif args['send']:
        return send(
                args['<to>'],
                args['<subject>'],
                args['--html'],
                args['--text'],
                args['--attachment']
                )
    elif args['send_template']:
        return send_template(
                args['<subject>'],
                args['<template.html>'],
                args['<data.csv>']
                )
    else:
        assert(False)

if __name__ == '__main__':
    pprint(main())
