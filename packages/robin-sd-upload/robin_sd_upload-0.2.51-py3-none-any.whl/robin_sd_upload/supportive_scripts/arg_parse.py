#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import argparse
import sys

from robin_sd_upload import _version
from robin_sd_upload.slack_interaction import slack_handler
from robin_sd_upload.supportive_scripts import yaml_parser
from robin_sd_upload.supportive_scripts import logger
from robin_sd_upload.supportive_scripts import version_checker

from robin_sd_upload.api_interaction import push_software
from robin_sd_upload.supportive_scripts import check_upload_file
from robin_sd_upload.supportive_scripts import validate
from robin_sd_upload.supportive_scripts import create_zip
from robin_sd_upload.supportive_scripts import remove_zip


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Robin Radar Systems - Software Uploader',
        usage='robin-sd-upload [options]',
        prog='Robin Radar Systems Software Uploader',
        epilog='To report any bugs or issues, please visit: \
        https://support.robinradar.systems or run: robin-sd-upload --slack'
    )

    parser.add_argument('-c', '--check', action='store_true',
                        help='ensure all prerequisites are met')
    parser.add_argument('-u', '--upload', action='store_true',
                        help='upload software: robin-sd-upload --upload --path=upload_folder_absolute_path')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(version=_version.__version__))
    parser.add_argument('-s', '--slack', action='store_true',
                        help='Send the logs to IT/DevOps Slack channel')

    # arguments for upload
    parser.add_argument('-p', "--path", type=str,
                        help="upload file absolute path")

    args = parser.parse_args()
    config = yaml_parser.parse_config()
    logger.log(message="Starting Robin Radar Systems Software Uploader",
               log_level="info", to_terminal=True)
    logger.log(message="Version: " + _version.__version__,
               log_level="info", to_terminal=True)
    logger.log(message="Username: " +
               config['robin_email'], log_level="info", to_terminal=True)

    version_checker.check_latest_version()

    if args.check:
        yaml_parser.parse_config()
        logger.log(message="All prerequisites met.",
                   log_level="info", to_terminal=True)
        sys.exit(0)
    elif args.upload:
        if args.path is None:
            print('Please provide the argument: --path')
            sys.exit(1)

        # extract radar type and version name from upload file path
        upload_file_path = args.path
        parts = upload_file_path.split('/')
        if len(parts) < 2:
            print('Please provide a valid upload file path.')
            sys.exit(1)
        radar_type = parts[-2]
        version_name = parts[-1]

        logger.log("Zipping file: " + upload_file_path,
                   log_level="info", to_terminal=False)
        logger.log("Radar type: " + radar_type,
                   log_level="info", to_terminal=False)
        logger.log("Version name: " + version_name,
                   log_level="info", to_terminal=False)
        logger.log("parts: " + str(parts),
                   log_level="info", to_terminal=False)

        # check if the radar type is valid
        validate.validate(radar_type, version_name)
        if check_upload_file.check_upload_file(upload_file_path) is False:
            sys.exit(1)

        # create a temp folder and zip the file
        temp_dir = tempfile.mkdtemp()
        zipped_file_path = temp_dir + '/' + version_name + '.zip'

        create_zip.create_zip(upload_file_path, temp_dir, version_name)
        push_software.push_software(zipped_file_path, radar_type, version_name)
        remove_zip.remove_zip(zipped_file_path)
        sys.exit(0)

    elif args.slack:
        slack_handler.send_slack_entrypoint()
        logger.log(message="Slack message sent successfully.",
                   log_level="info", to_terminal=True)
        sys.exit(0)

    else:
        parser.print_help()
        sys.exit(1)
