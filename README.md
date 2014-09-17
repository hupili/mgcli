# MailGun CLI

Simple CLI to play with MailGun

## Usage

First familiarize yourself with some backgrounds of MailGun,
e.g. via the official [quickstart guide](http://documentation.mailgun.com/quickstart.html)

Second, configure your domain and acquire `API_KEY` from the web UI of MailGun.

You're all set.
This small tool is just like any other CLI programs.

```
%python mgcli.py -h
Usage:
    mgcli.py config get
    mgcli.py config set <domain> <api_key> <from_address>
    mgcli.py send <to> <subject> [--html=<fn_html>] [--text=<fn_text>]
```

## License

MIT
