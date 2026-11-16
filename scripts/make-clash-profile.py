#!/usr/bin/env python3
"""Build a personal Clash Verge / mihomo profile from Shadowsocks links.

    python3 scripts/make-clash-profile.py -o private/clash-me.yaml 'ss://...' 'ss://...'
    sudo ss-list alice | python3 scripts/make-clash-profile.py -o private/clash-alice.yaml -

It fills clash/asia-direct.yaml with the nodes from the ss:// links (one node
per link; the name comes from the part after #). A single "-" reads text from
standard input and picks out every ss:// link in it.

The output holds the node passwords. Send it privately, like an ss:// link,
and never commit it: the private/ folder is ignored by git.
"""
from pathlib import Path
from urllib.parse import unquote
import argparse
import base64
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "clash" / "asia-direct.yaml"
LINK_RE = re.compile(r"ss://[^\s'\"<>]+")


def b64decode(text):
    text = text.replace("-", "+").replace("_", "/")
    return base64.b64decode(text + "=" * (-len(text) % 4)).decode("utf-8")


def parse_link(link):
    """Return a node dict from an ss:// link (SIP002 or the older all-base64 form)."""
    body = link[len("ss://"):]
    body, _, name = body.partition("#")
    body = body.partition("?")[0].rstrip("/")   # plugins are not supported
    if "@" not in body:                          # ss://BASE64(method:password@host:port)
        body = b64decode(body)
    userinfo, _, hostport = body.rpartition("@")
    if ":" not in userinfo:                      # ss://BASE64(method:password)@host:port
        userinfo = b64decode(unquote(userinfo))
    else:
        userinfo = unquote(userinfo)
    cipher, _, password = userinfo.partition(":")
    host, _, port = hostport.rpartition(":")
    host = host.strip("[]")
    if not (cipher and password and host and port.isdigit()):
        raise ValueError("not a usable ss:// link (method, password, host or port missing)")
    return {"name": unquote(name) or f"{host}:{port}", "server": host, "port": int(port),
            "cipher": cipher, "password": password}


def q(text):
    """A YAML double-quoted string (JSON strings are valid YAML)."""
    return json.dumps(text, ensure_ascii=False)


def replace_block(text, marker, lines):
    pattern = re.compile(r"(?m)^(?P<indent>[ ]*)# >>> %s.*\n(?:.*\n)*?[ ]*# <<< %s\n" % (marker, marker))
    match = pattern.search(text)
    if not match:
        raise SystemExit(f"{TEMPLATE}: marker '{marker}' not found")
    indent = match.group("indent")
    return text[:match.start()] + "".join(indent + line + "\n" for line in lines) + text[match.end():]


def build(nodes):
    text = TEMPLATE.read_text(encoding="utf-8")
    # Drop the "this is a template" lines of the header.
    text = re.sub(r"(?m)^# 這是「範本」.*\n(?:# .*\n)*?#\n", "", text, count=1)
    node_lines = []
    for node in nodes:
        node_lines += [f"- name: {q(node['name'])}", "  type: ss", f"  server: {q(node['server'])}",
                       f"  port: {node['port']}", f"  cipher: {q(node['cipher'])}",
                       f"  password: {q(node['password'])}", "  udp: true"]
    text = replace_block(text, "NODES", node_lines)
    text = replace_block(text, "EXIT", [f"- {q(node['name'])}" for node in nodes])
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("links", nargs="+", help="ss:// links, or - to read them from standard input")
    parser.add_argument("-o", "--output", required=True, help="file to write, for example private/clash-me.yaml")
    args = parser.parse_args()

    links = []
    for item in args.links:
        links += LINK_RE.findall(sys.stdin.read()) if item == "-" else [item]
    if not links:
        raise SystemExit("No ss:// link found.")
    nodes, seen = [], set()
    for number, link in enumerate(links, 1):
        if not link.startswith("ss://"):
            raise SystemExit(f"Link {number} does not start with ss://")
        try:
            node = parse_link(link)
        except Exception as error:            # never echo the link: it holds the password
            raise SystemExit(f"Link {number}: {error}")
        if node["name"] in seen:
            raise SystemExit(f"Link {number}: the node name '{node['name']}' is used twice")
        seen.add(node["name"])
        nodes.append(node)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(build(nodes))
    os.chmod(output, 0o600)
    print(f"Wrote {output} with {len(nodes)} node(s): " + ", ".join(node["name"] for node in nodes))
    print("It holds the node passwords: send it privately and do not commit it.")


if __name__ == "__main__":
    main()
