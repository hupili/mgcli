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
```

Or if you prefer dockerised environment:

```
docker run -v $HOME/.mgclirc:/root/.mgclirc --rm -it hupili/mgcli
```

## For maintainer

Rebuild the image:

```
docker build -t hupili/mgcli .
```

## License

MIT
