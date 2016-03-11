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

    parser = argparse.ArgumentParser(
        description=summary_usage, epilog=detailed_usage,
        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('-s', '--save-format', required=False, type=str,
                        metavar='save_format',
                        help='Save the documentation in the given format '
                             '(default: "only show links, do not save")')

    parser.add_argument('-d', '--destination-dir', required=False, type=str,
                        metavar='destination_dir',
                        help='Save the documentation(s) to this directory '
                             '(default: "save to current directory")')

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

    save_to_dir = None         # default if it is not asked to save any format
    if args.save_format:
        save_to_dir = args.destination_dir if args.destination_dir else '.'

    for slug in args.slugs:
        readthedocs_api(slug, args.no_comments, args.save_format, save_to_dir)


def readthedocs_api(slug, omit_comments, save_format, save_to_dir):
    """Queries and process the download links for the EPUB, HtmlZip, and PDF
    files of the project given by parameter 'slug'. If 'omit_comments' is
    False, it also prints comments on this project, as the time of last
    modification of the documentation of this project in ReadTheDocs.org and
    the source code repository for this project."""

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

                    dnld_url = 'https:' + val if val.startswith('//') else val

                    process_url_from_api(key.encode('UTF-8'), dnld_url, slug,
                                         save_format, save_to_dir)


def process_url_from_api(format_this_url, dnld_url, slug, save_format,
                         save_to_dir):
    """Process the download URL 'dnld_url' returned from the RTD.org API, of
    file format 'format_this_url'.
    The processing is either listing it or downloading it, if 'save_format' is
    requested."""

    # check if the format of this url is precisely the format requested to be
    # saved: if it is another format, then clear the format requested to be
    # saved. ('zip' is a special case: the RTD.org API answers format
    # 'htmlzip', but this program is simply requested to save the 'zip' format)
    if save_format != 'zip':
        save_format = None if save_format != format_this_url else save_format
    else:
        save_format = None if format_this_url != 'htmlzip' else save_format

    if save_format:
        http_res = requests.get(dnld_url, allow_redirects=True, stream=True)
    else:
        http_res = requests.head(dnld_url, allow_redirects=True)

    # pylint: disable=no-member
    exists = (http_res.status_code == requests.codes.ok)
    if exists:
        print("{}: {}: {}".format(slug, format_this_url, dnld_url))
        if save_format:
            dest_fname = '{}/{}.{}'.format(save_to_dir, slug, save_format)
            with open(dest_fname, 'wb') as dest_file:
                for chunk in http_res.iter_content(64 * 1024):
                    dest_file.write(chunk)
    else:
        print("{}: {}: {} [{}]".format(slug, format_this_url, dnld_url,
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
