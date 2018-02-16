# MailGun CLI

Simple CLI to play with MailGun

## Usage

Preparation:

* Familiarize yourself with some backgrounds of MailGun, e.g. via the official [quickstart guide](http://documentation.mailgun.com/quickstart.html)
* Configure your domain and acquire `API_KEY` from the web UI of MailGun.

You're all set.
This small tool is just like any other CLI programs.

```
python mgcli.py -h
```

Or if you prefer dockerised environment:

```
docker run -v $HOME/.mgcli/:/root/.mgcli/ -v $(pwd):/data/ --rm -it hupili/mgcli
```

* `-v $HOME/.mgcli/:/root/.mgcli/` mounts the configurations which will be stored at your `~/.mgcli/mgclirc`
* `-v $(pwd):/data/` mounts the current folder (where you run the container on host) to the working folder in container (i.e. `/data`)

## For maintainer

Rebuild the image:

```
docker build -t {image-name} .
```

There is now auto-build `hupili/mgcli` on dockerhub, so the `master` of this repo will be reflected in `hupili/mgcli:latest` automatically. The tags `/release-.*/` will also trigger auto-builds on dockerhub.

## License

MIT
