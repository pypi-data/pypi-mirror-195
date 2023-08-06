# Prisma2Markdown

Prisma2Markdown or more is a pure python package that aim to facilitate 
prisma database visualization using mermaid.

Unfortunately, mermaid still have an issue that prevent perfect visualization since mermaid cannot yet create attribute relations.
# Installation
```
pip install py-prisma2markdown
```
or 
```
pip install git+https://github.com/HOZHENWAI/py-prisma2markdown.git
```
# Usage
This package make a command line available:
```prisma2markdown ```

To use the ```prisma2markdown update``` command, you have to setup your markdown
with the following script:
```
\n[comment]: # (prisma2markdown)\n\n[comment]: # ({TARGET_PRISMA_SCRIPT})
```
replacing {TARGET_PRISMA_SCRIPT} with a path to the prisma script then calling
the cli command: ```prisma update --markdown-target PATH_TO_MARKDOWN```
