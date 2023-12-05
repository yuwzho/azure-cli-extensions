# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

import os
from knack.log import get_logger

from .base_transformer import Transformer

logger = get_logger(__name__)

DOCKER_PASSWORD_ENV_KEY = 'CF_DOCKER_PASSWORD'

class SourceTransformer(Transformer):

    def _check_pcf_to_bicep_violation(self, input, **__):
        for app in input.get('applications', []):
            self._check_path(app)
            self._check_docker_password(app)
    
    def _pcf_to_bicep(self, input, output, **__):
        for app in input.get('applications', []):
            resource = output.find('Microsoft.AppPlatform/Spring/Apps/Deployments', app.get('name', ''))
            if not resource:
                raise KeyError(f'Cannot find deployment resource {app.get("name")} in Bicep resources')
            self._parse_docker(app, resource)
            self._fallback(resource)

    def _parse_docker(self, app, resource):
        docker = self._get_docker(app)
        if docker:
            resource.put_properties('source', {
                'type': 'Container',
                'customContainer': docker
            })
    
    def _fallback(self, resource):
        if resource.get_property('source'):
            return
        resource.put_properties('source', {
            'type': 'BuildResult',
            'buildResultId': '<default>'
        })

    def _check_path(self, app):
        if app.get('path'):
            logger.error(f"App {app.get('name')} is deployed from local. Cannot convert to bicep.")

    def _check_docker_password(self, app):
        if app.get('docker', {}).get('username') and not os.getenv(DOCKER_PASSWORD_ENV_KEY):
            logger.error(f'App {app.get("name")} is deployed with docker image with authentication,' 
                         'but there is no docker registry password set through environment variable {DOCKER_PASSWORD_ENV_KEY}.')

    def _get_docker(self, app):
        docker = app.get('docker')
        if not docker:
            return
        image = app.get('docker').get('image')
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
        