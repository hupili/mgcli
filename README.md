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
docker run -v $HOME/.mgclirc:/root/.mgclirc -v $(pwd):/data/ --rm -it hupili/mgcli
```

Note, if you choose to run by docker, please `touch ~/.mgclirc` before the first execution. Or docker will likely create a directory at path `~/.mgclirc`, instead of a file.

## For maintainer

Rebuild the image:

```
docker build -t hupili/mgcli .
```

## License

MIT
