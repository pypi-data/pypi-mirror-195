#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import validators
from robin_sd_upload.supportive_scripts import logger


def validate(radarType, version_name):
    radarTypearray = ["elvira", "iris", "birdradar"]
    if validators.length(radarType, min=1, max=50) == False:
        logger.log(message="Radar type is not valid: " +
                   radarType, log_level="error", to_terminal=True)
        exit()
    if radarType not in radarTypearray:
        logger.log(message="Radar type is not valid: " +
                   radarType, log_level="error", to_terminal=True)
        exit()
    else:
        logger.log(message="Radar type is valid: " + radarType,
                   log_level="info", to_terminal=True)

    if validators.length(version_name, min=1, max=20) == False:
        logger.log(message="Version name is not valid: " +
                   version_name, log_level="error", to_terminal=True)
        exit()
    else:
        logger.log(message="Version name is valid: " +
                   version_name, log_level="info", to_terminal=True)
        return radarType, version_name
