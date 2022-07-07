#!/usr/bin/env python3
# usage:
# ./gen_readme.py > README.md
#
# requires pip install pyyaml

import yaml

# load paper specs
with open('papers.yml') as file_:
    papers = yaml.safe_load(file_)
    papers.sort(key=lambda p: p['year'])

# set computed fields
for paper in papers:
    author = paper['author'].split(',')[0].split(' ')[0].lower()
    year = str(paper['year'])[2:]
    paper['ref'] = f'{author}{year}'

# build table of contents
papers_toc = ''
for paper in papers:
    papers_toc += f'1. **{paper["title"]}**. [{paper["author"]} ({paper["year"]})]({paper["link"]}).\n'
    for related in sorted(paper.get('related', []), key=lambda p: p["year"]):
        papers_toc += f'    * {related["title"]}. [{related["author"]} ({related["year"]})]({related["link"]}).\n'

# build full flat list
for paper in papers:
    for rel in paper.get('related', []):
        papers.append(rel)

papers.sort(key=lambda p: p['year'])
papers_full = ''
for n, paper in enumerate(papers):
    papers_full += f'1. {paper["title"]}. [{paper["author"]} ({paper["year"]})]({paper["link"]})\n'


# inject into readme
with open('README.md.template') as template:
    # this (and the previous markdown) could be rewritten to use some templating engine,
    # but at this size I find it simpler to format manually
    output = template.read().\
        replace('{{ PAPERS_TOC }}', papers_toc).\
        replace('{{ PAPERS_FULL }}', papers_full)

print(output)
