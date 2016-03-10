#!/usr/bin/env python

# pylint: disable=line-too-long

"""List all the projects whose documentation is hosted by ReadTheDocs.org, so
you can find interesting software projects, that besides being Open Source,
have as well public documentation, like on LIGO:

   'description': 'geco_stat is a package created at Columbia for generating \
reports on data quality using recorded signals from \
LIGO's timing system and timing diagnostic system.',

   'subdomain': 'http://geco-statistics.readthedocs.org/',
   'project_url': 'http://geco.markalab.org',
   'repo': 'https://github.com/stefco/geco_stat.git',
   'modified_date': '2016-02-28T16:42:55.105561',
   'pub_date': '2016-02-23T12:46:43.902099',

and other 20'000 software projects."""

from __future__ import print_function
import logging
import json
import slumber


def main():
    """Main function."""

    import argparse
    from argparse import RawDescriptionHelpFormatter

    detailed_usage = get_this_script_docstring()

    summary_usage = 'List the attributes of all the projects hosted by ' \
                    'ReadTheDocs.org.'

    parser = argparse.ArgumentParser(
        description=summary_usage, epilog=detailed_usage,
        formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('-v', '--verbose', required=False,
                        dest='verbose', action='store_true',
                        help='Be verbose in the requests to the '
                             'ReadTheDocs.org API')
    parser.set_defaults(verbose=False)

    args = parser.parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.WARN

    logging.basicConfig(level=logging_level,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    list_attribs_all_readthedocs()


def list_attribs_all_readthedocs():
    """Print to the standard output all the projects hosted by
    ReadTheDocs.org and their attributes."""

    logging.debug("Connecting to the readthedocs.org API")

    api = slumber.API(base_url='http://readthedocs.org/api/v1/')

    window_offset = 0
    batch_limit = 20

    try:
        while True:
            logging.debug("Querying at offset %d limit %d", window_offset,
                          batch_limit)

            val = api.project.get(offset=window_offset, limit=batch_limit)

            if 'objects' in val:
                print(json.dumps(val['objects'], indent=4))

            if 'meta' in val and 'next' in val['meta']:
                # "next": "/api/v1/project/?limit=20&offset=20"
                url = val['meta']['next']
                url_params = url.split('?', 1)[-1]
                params = url_params.split('&')
                logging.debug("Got URL: '%s' with params '%s' and values '%s'",
                              url, repr(url_params), repr(params))
                for param in params:
                    if param.startswith('limit='):
                        batch_limit = int(param.split('=', 1)[-1])
                    if param.startswith('offset='):
                        window_offset = int(param.split('=', 1)[-1])
    except Exception as exc:     # pylint: disable=broad-except
        logging.error("Exception caught: %s", repr(exc))


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
