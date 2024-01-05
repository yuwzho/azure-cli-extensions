# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument, logging-format-interpolation, protected-access, wrong-import-order, too-many-lines

import os
import random, string
from knack.log import get_logger

from .base_transformer import PCFToBicepAppTransformer, BicepResourceType
from .pcf_resource import PCFParamRef
from .bicep_resource import BicepParam, BicepParamRef

logger = get_logger(__name__)

DOCKER_PASSWORD_ENV_KEY = 'CF_DOCKER_PASSWORD'


def _get_random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


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
        return app.find_value('docker')
    
    def _convert_pcf_value_to_bicep_value(self, docker):
        docker = self._parse_docker(docker)
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

    def _parse_docker(self, docker):
        if not docker:
            return
        image = docker.get('image')
        if not image:
            return
        docker_dict = self._parse_image(image)
        if docker.get('username'):
            docker_dict['imageRegistryCredential'] = {
                'username': docker.get('username'),
                'password': os.getenv(DOCKER_PASSWORD_ENV_KEY)
            }
        return docker_dict

    def _parse_image(self, image):
        if not image:
            return {}
        if isinstance(image, PCFParamRef):
            return self._parse_image_ref(image)
        registry, image_with_tag = image.split('/', 1)
        return {
            'server': registry,
            'containerImage': image_with_tag,
        }

    def _parse_image_ref(self, image_ref):
        if len(image_ref.contents) == 1:
            image_variable = image_ref.contents[0].value
            logger.warning(f'ASA Bicep requires the docker image write in ' + 
                           '{"server": "<registry server>", "containerImage": "<image>"} format. ' + 
                           f'Please update your parameter file for variable {image_variable} to ' +
                           f'{image_variable}_server and {image_variable}_image')
            return {
                'server': BicepParamRef(BicepParam(image_variable + '_server', 
                                                   'string', 'Deployed image registry server')),
                'containerImage': BicepParamRef(BicepParam(image_variable + '_image', 
                                                           'string', 'Deployed image without registry server'))
            }
        
        registry_params, container_image_params = self._split_image_ref(image_ref)

        if not registry_params or not container_image_params: # The parameter cannot be split into server and image part
            random_string = _get_random_string(4)
            result = {
                'server': BicepParamRef(BicepParam('registry_server_' + random_string, 
                                                   'string', 'Deployed image registry server')),
                'containerImage': BicepParamRef(BicepParam('container_image_' + random_string, 
                                                           'string', 'Deployed image without registry server'))
            }
            logger.warning(f'Cannot parse the image variable {str(image_ref)} to ASA Bicep resource. Please fulfill the ' + 
                           f'{str(result["server"])} and {str(result["containerImage"])}')
            return result
        
        return {
            'server': self._pcf_param_ref_to_bicep_param_ref(PCFParamRef(*registry_params)),
            'containerImage': self._pcf_param_ref_to_bicep_param_ref(PCFParamRef(*container_image_params))
        }

    def _split_image_ref(self, image_ref):
        registry = []
        image = []

        is_registry = True
        for x in image_ref.contents:
            if is_registry and isinstance(x, str) and '/' in x:
                is_registry = False
                registry_part, image_part = x.split('/', 1)
                if registry_part:
                    registry.append(registry_part)
                if image_part:
                    image.append(image_part)
            elif is_registry:
                registry.append(x)
            else:
                image.append(x)
        return registry, image