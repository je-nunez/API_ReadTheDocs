#!/bin/sh

./api_readthedocs.py scipy-cookbook numpy theanets python-aspectlib

./api_readthedocs.py --no-comments scipy-cookbook numpy theanets python-aspectlib

# list all the summaries of documentation of projects hosted in
# ReadTheDocs.org (giving description of the documentation,
# project names, time of last update of the documentation, and other
# attributes), saving it to a file

./ls_all_projects_rtd.py > /tmp/all_documentation_in_ReadTheDocs.txt

