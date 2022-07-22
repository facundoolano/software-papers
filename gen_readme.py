#!/usr/bin/env python3
# usage:
# ./gen_readme.py > README.md
#
# requires pip install pyyaml

import yaml


def load_papers():
    def markdown(paper, bold=False):
        title = f'**{paper["title"]}**' if bold else paper['title']
        return f'{title}. [{paper["author"]} ({paper["year"]})]({paper["link"]}).\n'

    with open('papers.yml') as file_:
        papers = yaml.safe_load(file_)

    for paper in papers:
        paper['markdown'] = markdown(paper, bold=True)
        for related in paper.setdefault('related', []):
            related['markdown'] = markdown(related, bold=False)

        paper['related'].sort(key=lambda p: p['year'])

    return papers


def render_readme(papers):
    with open('README.md.template') as template:
        readme = template.read()

    # Full nested list
    papers_full = ''
    for paper in papers:
        papers_full += '1. ' + paper['markdown']
        for related in paper['related']:
            papers_full += '    * ' + related['markdown']
    readme = readme.replace('{{ PAPERS_FULL }}', papers_full)

    # top-level only
    papers_top = ''
    for paper in papers:
        papers_top += '1. ' + paper['markdown']
    readme = readme.replace('{{ PAPERS_TOC }}', papers_top)

    # chronological flat list
    all_papers = []
    for paper in papers:
        all_papers.append(paper)
        all_papers += paper['related']

    papers_sorted = ''
    for paper in sorted(all_papers, key=lambda p: p['year']):
        papers_sorted += '1. ' + paper['markdown']
    readme = readme.replace('{{ PAPERS_SORTED }}', papers_sorted)

    return readme


if __name__ == '__main__':
    papers = load_papers()
    output = render_readme(papers)
    print(output)
