# mitmstatic
Converts a mitmproxy/mitmweb exported .dms file into a static website and Dockerfile.

# install
Easiest to use a Python 3 & pip3 environment and just run `pip3 install mitmstatic`.

# use

Just run `mitmstatic my.dms` and it will create a directory structure representing the capture, and will print to stdout a Dockerfile for encapsulating it.

Note that if your webserver has application/octet-stream set as its default mime type, big chunks of this may not work. Set the default to text/html and you should be fine. The Dockerfile does this for you :)
