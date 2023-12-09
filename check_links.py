#!/usr/bin/env python3
# checks that all links in the paper yaml are reachable
# requires pip install pyyaml requests


import requests
import yaml

HEADERS = {'User-Agent': 'My User Agent 1.0'}

with open('papers.yml') as file_:
    papers = yaml.safe_load(file_)

for paper in papers:
    papers += paper.get('related', [])


exit_code = 0
for paper in papers:
    ref = paper['author'].replace(',', '').split(' ')[0] + str(paper['year'])
    print(f'{ref}...', end='', flush=True)

    response = requests.head(paper['link'], headers=HEADERS)
    if response.status_code == 405:
        response = requests.get(paper['link'], headers=HEADERS)
    if response.ok:
        print('ok')
    else:
        exit_code = 1
        print(' ERROR')
        print(f'    failed fetching {paper["link"]}')

exit(exit_code)
