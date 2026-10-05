#!/bin/bash
# Regenerate the site and publish it to GitHub Pages (docs/). Set FACTORY=/path/to/byok-factory if it is not
# ../byok-factory next to this repo or /root/claude/Factory (see store_site.py).
cd "$(dirname "$0")" && python3 store_site.py && rm -rf docs/* && cp -r site/* docs/ && export GIT_COMMITTER_NAME=Mohithash GIT_COMMITTER_EMAIL=17986082+Mohithash@users.noreply.github.com && git add -A && git commit -q --author="Mohithash <17986082+Mohithash@users.noreply.github.com>" -m "${1:-Catalog update}" && git push -q origin main && echo published
