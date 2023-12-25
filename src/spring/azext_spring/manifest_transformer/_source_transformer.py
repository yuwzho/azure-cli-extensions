# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

import os
from knack.log import get_logger

from .base_transformer import PCFToBicepAppTransformer, BicepResourceType

logger = get_logger(__name__)

DOCKER_PASSWORD_ENV_KEY = 'CF_DOCKER_PASSWORD'

class SourceTransformer(PCFToBicepAppTransformer):
    @property
    def parsable_attributes(self):
        return ['docker'] 

    @property
    def _bicep_resource_type(self):
        return BicepResourceType.Deployment.value

    @property
    def _bicep_path(self):
        return 'source'

    def _check_pcf_to_bicep_violation(self, pcf, **__):
        for app in pcf.applications:
            self._check_docker_password(app)

    def _find_value_from_pcf(self, app):
        docker = self._get_docker(app)
        if docker:
            return {
                'type': 'Container',
                'customContainer': docker
            }
        else:
            return {
                'type': 'BuildResult',
                'buildResultId': '<default>'
            }

    def _check_docker_password(self, app):
        if app.find_value('docker.username') and not os.getenv(DOCKER_PASSWORD_ENV_KEY):
            logger.error(f'App {app.name} is deployed with docker image with authentication,' 
                         'but there is no docker registry password set through environment variable {DOCKER_PASSWORD_ENV_KEY}.')

    def _get_docker(self, app):
        docker = app.find_value('docker')
        if not docker:
            return
        image = docker.get('image')
        if not image:
            return
        registry, image_with_tag = image.split('/', 1)
        docker_dict = {
            'server': registry,
            'containerImage': image_with_tag,
        }
        if docker.get('username'):
            docker_dict['imageRegistryCredential'] = {
                'username': docker.get('username'),
                'password': os.getenv(DOCKER_PASSWORD_ENV_KEY)
            }
        return docker_dict
        