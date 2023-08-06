#!/usr/bin/env python3
import argparse
import os

from recollwebui import webui


def main():
    # handle command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--addr", default="127.0.0.1", help="address to bind to [127.0.0.1]"
    )
    parser.add_argument(
        "-p", "--port", default="8080", type=int, help="port to listen on [8080]"
    )
    parser.add_argument(
        "-c", "--config", default=None, type=str, help="configuration directory"
    )
    args = parser.parse_args()

    if args.config:
        os.environ["RECOLL_CONFDIR"] = args.config

    # set up webui and run in own http server
    webui.bottle.debug(True)
    webui.bottle.run(server="waitress", host=args.addr, port=args.port)


if __name__ == "__main__":
    main()

# vim: foldmethod=marker:filetype=python:textwidth=80:ts=4:et
