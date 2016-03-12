#!/bin/sh

./api_readthedocs.py scipy-cookbook numpy theanets python-aspectlib

./api_readthedocs.py --no-comments scipy-cookbook numpy theanets python-aspectlib

# If you want to download the documentation in pdf of hadoopy, scikit-cuda,
# flask and tornado to the directory ~/Documents/, run:

./api_readthedocs.py -s pdf -d ~/Documents/ hadoopy scikit-cuda flask tornado

# The files are saved with the same name as the project name in ReadTheDocs.org
# (Similar command to download the documentation in epub or zip, just change
#  the -s argument above correspondingly)

# list all the summaries of documentation of projects hosted in
# ReadTheDocs.org (giving description of the documentation,
# project names, time of last update of the documentation, and other
# attributes), saving it to a file

./ls_all_projects_rtd.py > /tmp/all_documentation_in_ReadTheDocs.txt

