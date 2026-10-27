#!/usr/bin/env python3
"""Observe diagnostic UDP heartbeats; this is not the RS-485 protocol parser."""

import argparse
import re
import socket


def port_number(value):
    port = int(value)
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be in 1..65535")
    return port


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bind", default="127.0.0.1", help="local IPv4; use the PC Ethernet IP for board tests")
    parser.add_argument("--port", type=port_number, default=4242)
    args = parser.parse_args()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as receiver:
            receiver.bind((args.bind, args.port))
            receiver.settimeout(0.5)
            print(f"Listening on {args.bind}:{args.port}; Ctrl+C to stop", flush=True)
            while True:
                try:
                    data, sender = receiver.recvfrom(65535)
                except socket.timeout:
                    continue
                message = data.decode("utf-8", errors="replace").rstrip("\r\n")
                match = re.search(r"(?:^|\s)seq=(\d+)(?=\s|$)", message)
                sequence = match.group(1) if match else "unavailable"
                # repr prevents control characters from manipulating the terminal.
                print(f"{sender[0]}:{sender[1]} seq={sequence} message={message!r}", flush=True)
    except KeyboardInterrupt:
        print("\nReceiver stopped", flush=True)
    except OSError as error:
        parser.exit(1, f"UDP receiver: {error}\n")


if __name__ == "__main__":
    main()
