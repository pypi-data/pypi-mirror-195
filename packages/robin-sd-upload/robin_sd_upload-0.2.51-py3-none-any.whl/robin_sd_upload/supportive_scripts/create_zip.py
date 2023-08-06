#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import zipfile

from robin_sd_upload.supportive_scripts import logger


def create_zip(directory, zipped_file_path, version_name):

    logger.log(message='Creating ZIP file from directory: ' + directory,
               log_level="info", to_terminal=True)
    logger.log(message='ZIP file path: ' + zipped_file_path,
               log_level="info", to_terminal=True)
    logger.log(message='Version name: ' + version_name,
               log_level="info", to_terminal=True)

    if os.path.exists(directory):
        logger.log(message="Directory exists: " + directory,
                   log_level="info", to_terminal=True)

        logger.log(message="Creating zip file: " + zipped_file_path,
                   log_level="info", to_terminal=True)

        # Create a ZipFile object
        zip_file = zipfile.ZipFile(os.path.join(
            zipped_file_path, version_name + ".zip"), "w")

        # Iterate over all the files in the directory
        for root, dirs, files in os.walk(directory):
            logger.log(message="Processing directory: " + root,
                       log_level="info", to_terminal=False)

            for file in files:
                # Get the file path
                file_path = os.path.join(root, file)
                logger.log(message="Processing file: " + file_path,
                           log_level="info", to_terminal=False)

                # Add the file to the zip file
                zip_file.write(file_path, os.path.join(
                    version_name, os.path.relpath(file_path, directory)))

        # Close the ZipFile
        zip_file.close()

        if os.path.getsize(zipped_file_path) > 0:
            logger.log(message="ZIP file created: " + os.path.join(zipped_file_path,
                       version_name + ".zip"), log_level="info", to_terminal=True)
        else:
            logger.log(message="ZIP file is empty: " + os.path.join(zipped_file_path,
                       version_name + ".zip"), log_level="error", to_terminal=True)

    else:
        logger.log(message="Directory does not exist: " +
                   directory, log_level="error", to_terminal=True)
