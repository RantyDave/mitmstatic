# Copyright (c) 2018 David Preece, All rights reserved.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
import sys
import os
from mitmproxy.io.io import read_flows_from_paths


def promote_to_index(dir):
    # turns out this one should be an index.html and not a static file
    with open(dir, 'r+b') as f:
        new_index = f.read()
    os.remove(dir)
    os.makedirs(dir, exist_ok=True)
    with open(dir + '/index.html', 'w+b') as f:
        f.write(new_index)


def main():
    if len(sys.argv) != 2:
        print("Usage: mitmstatic flow-file.dms")
        exit(1)

    # read and write the flows
    fqdn = None
    flows = read_flows_from_paths([sys.argv[1]])
    for flow in flows:
        path = flow.request.url.lstrip('http://')

        # get the fqdn
        if fqdn is None:
            fqdn = path[:path.find('/')]

        # get the path and filename
        directory = path[:path.rfind('/')]
        file = path[path.rfind('/')+1:]  # trailing slash means directory
        if file == '':
            file = 'index.html'
        localpath = directory + '/' + file

        # create the right directory
        try:
            os.makedirs(directory, exist_ok=True)
        except (NotADirectoryError, FileExistsError) as e:
            promote_to_index(directory)

        # write the file
        try:
            with open(localpath, 'w+b') as f:
                f.write(flow.response.content)
        # sometimes there are repeat flows, this is fine
        except (FileExistsError, IsADirectoryError):
            pass

    # emit a dockerfile
    print('FROM nginx')
    print('RUN sed -i -e \'s|default_type  application/octet-stream;|default_type text/html;|g\' /etc/nginx/nginx.conf')
    print("COPY %s/ /usr/share/nginx/html/" % fqdn)
