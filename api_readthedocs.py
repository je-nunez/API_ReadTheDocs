#!/usr/bin/env python

"""Show the download links to EPUB, HtmlZip, and PDF files of the
documentation of project hosted in ReadTheDocs.org."""

from __future__ import print_function
import requests
import slumber


def main():
    """Main function."""

    import argparse
    from argparse import RawDescriptionHelpFormatter

    detailed_usage = get_this_script_docstring()

    summary_usage = 'Retrieves download links to EPUB, HtmlZip, and PDF ' \
                    'documents of a project in ReadTheDocs.org.'

    parser = argparse.ArgumentParser(description=summary_usage,
                                     epilog=detailed_usage,
                                     formatter_class=
                                     RawDescriptionHelpFormatter)

    parser.add_argument('-n', '--no-comments', required=False,
                        dest='no_comments', action='store_true',
                        help='Do not print some of the header comments '
                             'related to the project in ReadTheDocs.org, '
                             'just print the URLs to download the documents.'
                             ' (default: "comments shown")')
    parser.set_defaults(no_comments=False)

    parser.add_argument('slugs', nargs='+',
                        help='the names of the projects in ReadTheDocs.org.')

    args = parser.parse_args()

    for slug in args.slugs:
        readthedocs_api(slug, args.no_comments)


def readthedocs_api(slug, omit_comments):
    """Reports the download links for the EPUB, HtmlZip, and PDF files of the
    project given by parameter 'slug'. If 'omit_comments' is False, it also
    prints comments on this project, as the time of last modification of the
    documentation of this project in ReadTheDocs.org and the source code
    repository for this project."""

    api = slumber.API(base_url='http://readthedocs.org/api/v1/')

    val = api.project.get(slug=slug)

    comment_keys = [
        {'rtd_key': 'project_url', 'msg': 'Project URL'},
        {'rtd_key': 'repo', 'msg': 'Code repository'},
        {'rtd_key': 'modified_date', 'msg': 'Doc last modification'},
        {'rtd_key': 'enable_epub_build', 'msg': 'Doc available as EPUB'},
        {'rtd_key': 'enable_pdf_build', 'msg': 'Doc available as PDF'}
    ]

    if 'objects' in val:
        for obj in val['objects']:

            if not omit_comments:
                for comment_key in comment_keys:
                    rtd_key = comment_key['rtd_key']
                    if rtd_key in obj and obj[rtd_key]:
                        msg = comment_key['msg']
                        print("{}: {}: {}".format(slug, msg, obj[rtd_key]))

            if 'downloads' in obj and isinstance(obj['downloads'], dict):
                for key, val in obj['downloads'].items():
                    # if key == 'pdf' and 'enable_pdf_build' in obj and \
                    #    not obj['enable_pdf_build']:
                    #    continue    # PDF generation disabled
                    # if key == 'epub' and 'enable_epub_build' in obj and \
                    #    not obj['enable_epub_build']:
                    #    continue    # EPUB generation disabled

                    dnld_url = 'https:' + val if val.startswith('//') else val

                    http_res = requests.head(dnld_url, allow_redirects=True)
                    # requests.get() will download the link (not save it
                    # though)
                    # ... = requests.get(dnld_url, allow_redirects=True)
                    # pylint: disable=no-member
                    exists = (http_res.status_code == requests.codes.ok)
                    if exists:
                        print("{}: {}: {}".format(slug, key, dnld_url))
                    else:
                        print("{}: {}: {} [{}]".format(slug, key, dnld_url,
                                                       exists))


def get_this_script_docstring():
    """Utility function to get the Python docstring of this script"""
    import os
    import inspect

    current_python_script_pathname = inspect.getfile(inspect.currentframe())
    dummy_pyscript_dirname, pyscript_filename = (
        os.path.split(os.path.abspath(current_python_script_pathname)))
    pyscript_filename = os.path.splitext(pyscript_filename)[0]  # no extension
    pyscript_metadata = __import__(pyscript_filename)
    pyscript_docstring = pyscript_metadata.__doc__
    return pyscript_docstring


if __name__ == '__main__':
    main()
