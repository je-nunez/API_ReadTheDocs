# Description

Gives the EPUB, HTML-ZIP and PDF direct links to download the documentation of
a project hosted by ReadTheDocs.org, so the documentation in any format can be
downloaded from ReadTheDocs.org.

It uses the useful ReadTheDocs.org's API, explained at
[http://read-the-docs.readthedocs.org/en/latest/api.html](http://read-the-docs.readthedocs.org/en/latest/api.html)

# WIP

This project is a *work in progress*. The implementation is *incomplete* and
subject to change. The documentation can be inaccurate.

# Usage and Example

To obtain the EPUB, HTML-Zip and PDF download links to the documentation of a
project hosted by ReadTheDocs.org whose name is
`https://<the-project-name>.ReadTheDocs.org/`, use:

     ./api_readthedocs.py  '<the-project-name>'  [...<other-project-names>...]

For example, to obtain the EPUB, HTML-Zip and PDF download links of the
documentation of the projects hosted by ReadTheDocs.org `scipy-cookbook`,
`numpy`, `theanets`, and `python-aspectlib`, use:

     ./api_readthedocs.py scipy-cookbook numpy theanets python-aspectlib

It will return as output:

     scipy-cookbook: Code repository: https://github.com/pv/SciPy-CookBook
     scipy-cookbook: Doc last modification: 2015-10-29T18:14:53.524239
     scipy-cookbook: pdf: https://readthedocs.org/projects/scipy-cookbook/downloads/pdf/latest/
     scipy-cookbook: htmlzip: https://readthedocs.org/projects/scipy-cookbook/downloads/htmlzip/latest/
     scipy-cookbook: epub: https://readthedocs.org/projects/scipy-cookbook/downloads/epub/latest/
     numpy: Project URL: http://numpy.org/
     numpy: Code repository: git://github.com/numpy/numpy.git
     numpy: Doc last modification: 2015-10-03T13:54:35.478615
     numpy: Doc available as EPUB: True
     numpy: Doc available as PDF: True
     numpy: pdf: https://readthedocs.org/projects/numpy/downloads/pdf/latest/
     numpy: htmlzip: https://readthedocs.org/projects/numpy/downloads/htmlzip/latest/
     numpy: epub: https://readthedocs.org/projects/numpy/downloads/epub/latest/
     theanets: Code repository: https://github.com/lmjohns3/theanets
     theanets: Doc last modification: 2015-12-03T14:44:14.632826
     theanets: pdf: https://readthedocs.org/projects/theanets/downloads/pdf/stable/ [False]
     theanets: htmlzip: https://readthedocs.org/projects/theanets/downloads/htmlzip/stable/
     theanets: epub: https://readthedocs.org/projects/theanets/downloads/epub/stable/
     python-aspectlib: Project URL: https://github.com/ionelmc/python-aspectlib
     python-aspectlib: Code repository: https://github.com/ionelmc/python-aspectlib.git
     python-aspectlib: Doc last modification: 2015-08-21T06:56:38.922584
     python-aspectlib: Doc available as EPUB: True
     python-aspectlib: Doc available as PDF: True
     python-aspectlib: pdf: https://readthedocs.org/projects/python-aspectlib/downloads/pdf/latest/
     python-aspectlib: htmlzip: https://readthedocs.org/projects/python-aspectlib/downloads/htmlzip/latest/
     python-aspectlib: epub: https://readthedocs.org/projects/python-aspectlib/downloads/epub/latest/

ReadTheDocs.org redirects the above directory links to the proper file in that format. E.g., it
redirects

     scipy-cookbook: epub: https://readthedocs.org/projects/scipy-cookbook/downloads/epub/latest/

to the EPUB file with the documentation of `scipy-cookbook`.

**Note**: Not all projects have their documentations available to be downloaded in
all the three formats, EPUB, PDF and HTML-Zip. This is owner-configurable per project
and per export-format in the hosting provided by ReadTheDocs.org. (Old projects, like
`scipy-cookbook`, neither have the attribute to indicate if the documentation is
available in that format, so what this program does is to do `HEAD` HTTP request to
the links returned, to ensure these links does exist. It could also have done a
`GET` HTTP request, but this would have implied to download directly that EPUB, PDF
and/or HTML-Zip, if available, using more network bandwith and running more slowly.)

Note that besides the download links, like:

     numpy: pdf: https://readthedocs.org/projects/numpy/downloads/pdf/latest/

     theanets: epub: https://readthedocs.org/projects/theanets/downloads/epub/stable/

it will also give the Project, Code Repository, and Time of Last Modification of the
documentation. If you want to omit these comments in the output, simply call the
program with the argument `--no-comments`, and it will give merely the links to
download the documentation in the EPUB, PDF, and/or HTML-Zip formats.

# List of all ReadTheDocs.org's hosted documentation

There is a second program in this repository, `ls_all_projects_rtd.py`, which will contact
ReadTheDocs.org's API and will return the list of all the documentation hosted in this site,
including all attributes as above (time of last update of the documentation, source code
repositories, etc) and others, like initial publication date of the documentation, etc.

This program is useful because it gives a quick browse which can reveal very interesting
projects which have documentation in ReadTheDocs.org and can be interesting to see its
functionality or implementation, like, to name just a few of the more than 28'000 projects
whose documentation is hosted there:

     geco-statistics  (a Python 2.6+ module to analyze results from LIGO interferometers,
                       of gravitational waves' fame. Details are in the documentation)

     platformio  (programming for the Internet of Things)

     gpiozero

     a-little-book-of-r-for-biomedical-statistics

     a-little-book-of-r-for-bayesian-statistics

     scikit-neuralnetwork

     raspberry-pi-guide

     auto-sklearn

# Requeriments:

The [slumber](https://pypi.python.org/pypi/slumber) and [requests](https://pypi.python.org/pypi/requests)
Python libraries.

# Other

ReadTheDocs.org has more structured access, like [http://docs.readthedocs.org/en/latest/api/projects.html](http://docs.readthedocs.org/en/latest/api/projects.html)

