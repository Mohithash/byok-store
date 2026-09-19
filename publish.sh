#!/bin/bash
cd /root/claude/Store && python3 store_site.py && rm -rf docs/* && cp -r site/* docs/ && export GIT_COMMITTER_NAME=Mohithash GIT_COMMITTER_EMAIL=17986082+Mohithash@users.noreply.github.com && git add -A && git commit -q --author="Mohithash <17986082+Mohithash@users.noreply.github.com>" -m "${1:-Catalog update}" && git push -q origin main && echo published
