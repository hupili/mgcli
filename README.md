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

Note, if you choose to run by docker, please `echo '{}' > ~/.mgclirc` before the first execution. This command basically creates an empty configuratoin files mgcli tool. Or docker will likely create a directory at path `~/.mgclirc`, instead of a file.

## For maintainer

Rebuild the image:

```
docker build -t {image-name} .
```

There is now auto-build `hupili/mgcli` on dockerhub, so the `master` of this repo will be reflected in `hupili/mgcli:latest` automatically. The tags `/release-.*/` will also trigger auto-builds on dockerhub.

## License

MIT
