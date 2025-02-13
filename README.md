# Extractous API

This is a simple wrapper around the [Extractous]() library, which is supposed to replace on [unstructured.io]() and be a bazillion
times faster.



## Docker

**Build**

```bash
docker build . -t $(basename $PWD)
```


**Run as API**

```bash
docker run --rm -p 8080:8080 -e JWT_SECRET=shhhhh -v $PWD:/app $_
```

Open http://localhost:8080 in your browser to read the basic docs and try the 'xml' endpoint.

**Run as CLI**

```bash
docker run -it --rm -v /path/to/data:/var/data $_ uv run app.py --input /var/data/yourfile.pdf
```
