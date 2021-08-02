import argparse
import sys
import re
import os

from s2angs import (gen_s2_ang_from_xml,
                    gen_s2_ang_from_zip,
                    gen_s2_ang_from_SAFE)


ZIP_RE = re.compile(r'\.zip$', re.IGNORECASE)
SAFE_RE = re.compile(r'\.SAFE$', re.IGNORECASE)
XML_RE = re.compile(r'\.xml$', re.IGNORECASE)


def main():
    parser = argparse.ArgumentParser(
        description="Generate sun and view angle bands for Sentinel 2")

    parser.add_argument('s2_path',
                        type=str,
                        help="Sentinel 2 input path (one of '.SAFE' folder, "
                             "'MTD_TL.xml' file, or a zipped '.SAFE' folder)")
    parser.add_argument("-o", "--outdir",
                        type=str,
                        required=False,
                        help="Output directory for generated angle bands")

    generate_anglebands(**vars(parser.parse_args()))

    return 0


def generate_anglebands(s2_path, outdir=None):
    '''
    Generate Sentinel 2 angle band files using MTD_TL.xml, or .SAFE,
    or a SAFE .zip

    Returns: str, str, str, str: path to solar zenith image, path to
       solar azimuth image, path to view (sensor) zenith image and
       path to view (sensor) azimuth image, respectively.
    '''
    generation_function = None
    if re.search(XML_RE, s2_path):
        generation_function = gen_s2_ang_from_xml
    elif re.search(SAFE_RE, s2_path):
        generation_function = gen_s2_ang_from_SAFE
    elif re.search(ZIP_RE, s2_path):
        generation_function = gen_s2_ang_from_zip
    else:
        raise RuntimeError("Can't infer S2 path type (expecting '.SAFE', "
                           "'.xml' or '.zip' extension)")

    if outdir is not None:
        os.makedirs(outdir, exist_ok=True)

    return generation_function(s2_path, outdir=outdir)


if __name__ == "__main__":
    sys.exit(main())
