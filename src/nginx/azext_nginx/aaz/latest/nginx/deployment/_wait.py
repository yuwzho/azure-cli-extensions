# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "nginx deployment wait",
)
class Wait(AAZWaitCommand):
    """Place the CLI in a waiting state until a condition is met.
    """

    _aaz_info = {
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/nginx.nginxplus/nginxdeployments/{}", "2024-11-01-preview"],
        ]
    }

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.deployment_name = AAZStrArg(
            options=["-n", "--name", "--deployment-name"],
            help="The name of targeted Nginx deployment",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^([a-z0-9A-Z][a-z0-9A-Z-]{0,28}[a-z0-9A-Z]|[a-z0-9A-Z])$",
            ),
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.DeploymentsGet(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=False)
        return result

    class DeploymentsGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Nginx.NginxPlus/nginxDeployments/{deploymentName}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "deploymentName", self.ctx.args.deployment_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2024-11-01-preview",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()

            _schema_on_200 = cls._schema_on_200
            _schema_on_200.id = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.identity = AAZIdentityObjectType()
            _schema_on_200.location = AAZStrType()
            _schema_on_200.name = AAZStrType(
                flags={"read_only": True},
            )
            _schema_on_200.properties = AAZObjectType()
            _schema_on_200.sku = AAZObjectType()
            _schema_on_200.system_data = AAZObjectType(
                serialized_name="systemData",
                flags={"read_only": True},
            )
            _schema_on_200.tags = AAZDictType()
            _schema_on_200.type = AAZStrType(
                flags={"read_only": True},
            )

            identity = cls._schema_on_200.identity
            identity.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )
            identity.tenant_id = AAZStrType(
                serialized_name="tenantId",
                flags={"read_only": True},
            )
            identity.type = AAZStrType()
            identity.user_assigned_identities = AAZDictType(
                serialized_name="userAssignedIdentities",
            )

            user_assigned_identities = cls._schema_on_200.identity.user_assigned_identities
            user_assigned_identities.Element = AAZObjectType()

            _element = cls._schema_on_200.identity.user_assigned_identities.Element
            _element.client_id = AAZStrType(
                serialized_name="clientId",
                flags={"read_only": True},
            )
            _element.principal_id = AAZStrType(
                serialized_name="principalId",
                flags={"read_only": True},
            )

            properties = cls._schema_on_200.properties
            properties.auto_upgrade_profile = AAZObjectType(
                serialized_name="autoUpgradeProfile",
            )
            properties.dataplane_api_endpoint = AAZStrType(
                serialized_name="dataplaneApiEndpoint",
                flags={"read_only": True},
            )
            properties.enable_diagnostics_support = AAZBoolType(
                serialized_name="enableDiagnosticsSupport",
            )
            properties.ip_address = AAZStrType(
                serialized_name="ipAddress",
                flags={"read_only": True},
            )
            properties.logging = AAZObjectType()
            properties.network_profile = AAZObjectType(
                serialized_name="networkProfile",
            )
            properties.nginx_app_protect = AAZObjectType(
                serialized_name="nginxAppProtect",
            )
            properties.nginx_version = AAZStrType(
                serialized_name="nginxVersion",
                flags={"read_only": True},
            )
            properties.provisioning_state = AAZStrType(
                serialized_name="provisioningState",
                flags={"read_only": True},
            )
            properties.scaling_properties = AAZObjectType(
                serialized_name="scalingProperties",
            )
            properties.user_profile = AAZObjectType(
                serialized_name="userProfile",
            )

            auto_upgrade_profile = cls._schema_on_200.properties.auto_upgrade_profile
            auto_upgrade_profile.upgrade_channel = AAZStrType(
                serialized_name="upgradeChannel",
                flags={"required": True},
            )

            logging = cls._schema_on_200.properties.logging
            logging.storage_account = AAZObjectType(
                serialized_name="storageAccount",
            )

            storage_account = cls._schema_on_200.properties.logging.storage_account
            storage_account.account_name = AAZStrType(
                serialized_name="accountName",
            )
            storage_account.container_name = AAZStrType(
                serialized_name="containerName",
            )

            network_profile = cls._schema_on_200.properties.network_profile
            network_profile.front_end_ip_configuration = AAZObjectType(
                serialized_name="frontEndIPConfiguration",
            )
            network_profile.network_interface_configuration = AAZObjectType(
                serialized_name="networkInterfaceConfiguration",
            )

            front_end_ip_configuration = cls._schema_on_200.properties.network_profile.front_end_ip_configuration
            front_end_ip_configuration.private_ip_addresses = AAZListType(
                serialized_name="privateIPAddresses",
            )
            front_end_ip_configuration.public_ip_addresses = AAZListType(
                serialized_name="publicIPAddresses",
            )

            private_ip_addresses = cls._schema_on_200.properties.network_profile.front_end_ip_configuration.private_ip_addresses
            private_ip_addresses.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.network_profile.front_end_ip_configuration.private_ip_addresses.Element
            _element.private_ip_address = AAZStrType(
                serialized_name="privateIPAddress",
            )
            _element.private_ip_allocation_method = AAZStrType(
                serialized_name="privateIPAllocationMethod",
            )
            _element.subnet_id = AAZStrType(
                serialized_name="subnetId",
            )

            public_ip_addresses = cls._schema_on_200.properties.network_profile.front_end_ip_configuration.public_ip_addresses
            public_ip_addresses.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.network_profile.front_end_ip_configuration.public_ip_addresses.Element
            _element.id = AAZStrType()

            network_interface_configuration = cls._schema_on_200.properties.network_profile.network_interface_configuration
            network_interface_configuration.subnet_id = AAZStrType(
                serialized_name="subnetId",
            )

            nginx_app_protect = cls._schema_on_200.properties.nginx_app_protect
            nginx_app_protect.web_application_firewall_settings = AAZObjectType(
                serialized_name="webApplicationFirewallSettings",
                flags={"required": True},
            )
            nginx_app_protect.web_application_firewall_status = AAZObjectType(
                serialized_name="webApplicationFirewallStatus",
                flags={"read_only": True},
            )

            web_application_firewall_settings = cls._schema_on_200.properties.nginx_app_protect.web_application_firewall_settings
            web_application_firewall_settings.activation_state = AAZStrType(
                serialized_name="activationState",
            )

            web_application_firewall_status = cls._schema_on_200.properties.nginx_app_protect.web_application_firewall_status
            web_application_firewall_status.attack_signatures_package = AAZObjectType(
                serialized_name="attackSignaturesPackage",
                flags={"read_only": True},
            )
            _WaitHelper._build_schema_web_application_firewall_package_read(web_application_firewall_status.attack_signatures_package)
            web_application_firewall_status.bot_signatures_package = AAZObjectType(
                serialized_name="botSignaturesPackage",
                flags={"read_only": True},
            )
            _WaitHelper._build_schema_web_application_firewall_package_read(web_application_firewall_status.bot_signatures_package)
            web_application_firewall_status.component_versions = AAZObjectType(
                serialized_name="componentVersions",
                flags={"read_only": True},
            )
            web_application_firewall_status.threat_campaigns_package = AAZObjectType(
                serialized_name="threatCampaignsPackage",
                flags={"read_only": True},
            )
            _WaitHelper._build_schema_web_application_firewall_package_read(web_application_firewall_status.threat_campaigns_package)

            component_versions = cls._schema_on_200.properties.nginx_app_protect.web_application_firewall_status.component_versions
            component_versions.waf_engine_version = AAZStrType(
                serialized_name="wafEngineVersion",
                flags={"required": True},
            )
            component_versions.waf_nginx_version = AAZStrType(
                serialized_name="wafNginxVersion",
                flags={"required": True},
            )

            scaling_properties = cls._schema_on_200.properties.scaling_properties
            scaling_properties.auto_scale_settings = AAZObjectType(
                serialized_name="autoScaleSettings",
                flags={"client_flatten": True},
            )
            scaling_properties.capacity = AAZIntType()

            auto_scale_settings = cls._schema_on_200.properties.scaling_properties.auto_scale_settings
            auto_scale_settings.profiles = AAZListType(
                flags={"required": True},
            )

            profiles = cls._schema_on_200.properties.scaling_properties.auto_scale_settings.profiles
            profiles.Element = AAZObjectType()

            _element = cls._schema_on_200.properties.scaling_properties.auto_scale_settings.profiles.Element
            _element.capacity = AAZObjectType(
                flags={"required": True},
            )
            _element.name = AAZStrType(
                flags={"required": True},
            )

            capacity = cls._schema_on_200.properties.scaling_properties.auto_scale_settings.profiles.Element.capacity
            capacity.max = AAZIntType(
                flags={"required": True},
            )
            capacity.min = AAZIntType(
                flags={"required": True},
            )

            user_profile = cls._schema_on_200.properties.user_profile
            user_profile.preferred_email = AAZStrType(
                serialized_name="preferredEmail",
            )

            sku = cls._schema_on_200.sku
            sku.name = AAZStrType(
                flags={"required": True},
            )

            system_data = cls._schema_on_200.system_data
            system_data.created_at = AAZStrType(
                serialized_name="createdAt",
            )
            system_data.created_by = AAZStrType(
                serialized_name="createdBy",
            )
            system_data.created_by_type = AAZStrType(
                serialized_name="createdByType",
            )
            system_data.last_modified_at = AAZStrType(
                serialized_name="lastModifiedAt",
            )
            system_data.last_modified_by = AAZStrType(
                serialized_name="lastModifiedBy",
            )
            system_data.last_modified_by_type = AAZStrType(
                serialized_name="lastModifiedByType",
            )

            tags = cls._schema_on_200.tags
            tags.Element = AAZStrType()

            return cls._schema_on_200


class _WaitHelper:
    """Helper class for Wait"""

    _schema_web_application_firewall_package_read = None

    @classmethod
    def _build_schema_web_application_firewall_package_read(cls, _schema):
        if cls._schema_web_application_firewall_package_read is not None:
            _schema.revision_datetime = cls._schema_web_application_firewall_package_read.revision_datetime
            _schema.version = cls._schema_web_application_firewall_package_read.version
            return

        cls._schema_web_application_firewall_package_read = _schema_web_application_firewall_package_read = AAZObjectType(
            flags={"read_only": True}
        )

        web_application_firewall_package_read = _schema_web_application_firewall_package_read
        web_application_firewall_package_read.revision_datetime = AAZStrType(
            serialized_name="revisionDatetime",
            flags={"required": True},
        )
        web_application_firewall_package_read.version = AAZStrType(
            flags={"required": True},
        )

        _schema.revision_datetime = cls._schema_web_application_firewall_package_read.revision_datetime
        _schema.version = cls._schema_web_application_firewall_package_read.version


__all__ = ["Wait"]
