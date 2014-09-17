import sys
from os import path
import docopt
import requests
import json
from pprint import pprint

DOC = '''
Usage:
    {0} config get
    {0} config set <domain> <api_key> <from_address>
    {0} send <to> <subject> [--html=<fn_html>] [--text=<fn_text>]
'''.format(path.basename(__file__))


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


def send(to, subject, html=None, text=None):
    config = load_config()
    url = 'https://api.mailgun.net/v2/%s/messages' % config['domain']
    data={'from': config['from_address'],
            'to': to,
            'subject': subject}
    if html:
        data.update({
            'html': open(html).read()
            })
    elif text:
        data.update({
            'text': open(text).read()
            })
    else:
        pprint('Warning: No email body is defined. Will send null message.')
        data.update({
            'text': ''
            })
    re = requests.post(url,
            auth=('api', config['api_key']),
            data=data)
    return {
            'data': data,
            'result': re
            }


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
        return send(args['<to>'], args['<subject>'], args['--html'], args['--text'])
    else:
        assert(False)

if __name__ == '__main__':
    pprint(main())
