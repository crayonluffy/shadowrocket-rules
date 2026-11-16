#!/usr/bin/env python3
"""Checks for the configs, the hand-written rule lists and the docs.

Run from anywhere:  python3 scripts/check.py
Exit code 0 means every check passed. It needs no network.
"""
from pathlib import Path
import ipaddress
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO_RAW = "https://raw.githubusercontent.com/crayonluffy/shadowrocket-rules/main/"
POLICIES = {"PROXY", "DIRECT", "REJECT", "TAILSCALE"}
RULE_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD",
              "IP-CIDR", "IP-CIDR6", "IP-ASN", "GEOIP", "USER-AGENT",
              "URL-REGEX", "RULE-SET", "FINAL"}
TAILSCALE_NET = ipaddress.ip_network("100.64.0.0/10")
# Configs that route the Tailscale range: file name -> policy it must use.
TAILNET_CONFIGS = {"ai-tailscale.conf": "TAILSCALE", "ai-tailnet-via-node.conf": "PROXY"}

errors = []


def fail(path, message):
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def parse_conf(path):
    """Return (general: dict, rules: list of field lists)."""
    general, rules, section = {}, [], None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("["):
            section = line.strip("[]")
        elif section == "General" and "=" in line:
            key, _, value = line.partition("=")
            general[key.strip()] = value.strip()
        elif section == "Rule":
            rules.append([field.strip() for field in line.split(",")])
    return general, rules


def networks(value):
    found = []
    for item in value.split(","):
        try:
            found.append(ipaddress.ip_network(item.strip(), strict=False))
        except ValueError:
            pass  # host names such as localhost, *.local
    return found


def check_config(path):
    general, rules = parse_conf(path)
    if not general:
        fail(path, "no [General] section")
    if not rules:
        fail(path, "no [Rule] section")
        return None
    for rule in rules:
        if rule[0] not in RULE_TYPES:
            fail(path, f"unknown rule type: {','.join(rule)}")
        policy = rule[1] if rule[0] == "FINAL" else (rule[2] if len(rule) > 2 else "")
        if policy not in POLICIES:
            fail(path, f"unknown or missing policy: {','.join(rule)}")
        if rule[0] == "RULE-SET":
            url = rule[1]
            if not url.startswith(REPO_RAW):
                fail(path, f"RULE-SET does not point at this repo: {url}")
            else:
                name = url[len(REPO_RAW):]
                source = ROOT / "sources" / (Path(name).stem + ".txt")
                if not (ROOT / name).exists() and not source.exists():
                    fail(path, f"RULE-SET file is not built by this repo: {name}")
    if rules[-1][0] != "FINAL":
        fail(path, "the last rule must be FINAL")
    if sum(rule[0] == "FINAL" for rule in rules) != 1:
        fail(path, "exactly one FINAL rule is needed")

    excluded = networks(general.get("bypass-tun", "") + "," + general.get("tun-excluded-routes", ""))
    covers_tailscale = any(net.version == 4 and net.overlaps(TAILSCALE_NET) for net in excluded)
    wanted = TAILNET_CONFIGS.get(path.name)
    tailnet_rules = [rule for rule in rules
                     if rule[:2] in (["DOMAIN-SUFFIX", "ts.net"], ["IP-CIDR", "100.64.0.0/10"])]
    if wanted:
        if covers_tailscale:
            fail(path, "100.64.0.0/10 must not be in bypass-tun: Tailscale traffic would skip the rules")
        if len(tailnet_rules) != 2:
            fail(path, "needs DOMAIN-SUFFIX,ts.net and IP-CIDR,100.64.0.0/10 rules")
        for rule in tailnet_rules:
            if rule[2] != wanted:
                fail(path, f"Tailscale rule must use {wanted}: {','.join(rule)}")
            if rule[0] == "IP-CIDR" and rule[-1] != "no-resolve":
                fail(path, "the 100.64.0.0/10 rule needs no-resolve")
            if rules.index(rule) > min(i for i, r in enumerate(rules) if r[0] == "RULE-SET"):
                fail(path, "Tailscale rules must come before the RULE-SET line")
    elif tailnet_rules or any("TAILSCALE" in rule for rule in rules):
        fail(path, "Tailscale rules belong only in " + ", ".join(sorted(TAILNET_CONFIGS)))
    return rules


def check_extras(path):
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        fields = [field.strip() for field in line.split(",")]
        if fields[0] not in RULE_TYPES - {"RULE-SET", "FINAL"}:
            fail(path, f"line {number}: unknown rule type: {line}")
        elif len(fields) < 2 or not fields[1]:
            fail(path, f"line {number}: missing value: {line}")
        elif fields[-1].upper() in POLICIES:
            fail(path, f"line {number}: a list must not name a policy (the .conf decides): {line}")


def check_links(path):
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
            continue
        if not (path.parent / target.partition("#")[0]).exists():
            fail(path, f"link to a file that does not exist: {target}")
    for name in re.findall(re.escape(REPO_RAW) + r"([\w./-]+)", text):
        source = ROOT / "sources" / (Path(name).stem + ".txt")
        if not (ROOT / name).exists() and not source.exists():
            fail(path, f"raw URL to a file that does not exist: {name}")


def main():
    configs = sorted((ROOT / "configs").glob("*.conf"))
    if not configs:
        errors.append("configs/: no .conf files")
    failsafes = {}
    for path in configs:
        rules = check_config(path)
        if rules and any(rule[0] == "RULE-SET" and rule[1].endswith("/ai.list") for rule in rules):
            failsafes[path] = sorted(",".join(rule) for rule in rules
                                     if rule[0] == "DOMAIN-SUFFIX" and rule[-1] == "REJECT")
    # Every AI config carries the same failsafe block as ai-only.conf.
    reference = failsafes.get(ROOT / "configs" / "ai-only.conf")
    for path, block in failsafes.items():
        if not block:
            fail(path, "no failsafe REJECT rules for the core AI domains")
        elif reference and block != reference:
            fail(path, "failsafe REJECT rules differ from configs/ai-only.conf")

    for path in sorted((ROOT / "extras").glob("*.list")):
        check_extras(path)
    for path in sorted((ROOT / "sources").glob("*.txt")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("https://"):
                fail(path, f"not an https URL: {line}")
    for path in [ROOT / "README.md"] + sorted((ROOT / "docs").glob("*.md")):
        check_links(path)

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s)")
        return 1
    print(f"OK: {len(configs)} configs, extras, sources and docs checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
