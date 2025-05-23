# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long

from azure.cli.core.commands.parameters import (
    get_generic_completion_list,
    get_resource_name_completion_list,
    quotes,
    resource_group_name_type,
)
from knack.arguments import CLIArgumentType
from azext_load.data_plane.utils import completers, models, utils, validators
from azext_load.vendored_sdks.loadtesting.models._enums import WeekDays, Frequency, TriggerState
from azext_load.data_plane.load_trigger import utils as trigger_utils

quote_text = f"Use {quotes} to clear existing {{}}."

# Common arguments
resource_group = resource_group_name_type

load_test_resource = CLIArgumentType(
    options_list=["--load-test-resource", "--name", "-n"],
    type=str,
    required=True,
    completer=get_resource_name_completion_list("Microsoft.LoadTestService/LoadTests"),
    help="Name or ARM resource ID of the Load Testing resource.",
)

custom_no_wait = CLIArgumentType(
    options_list=["--no-wait"],
    action="store_true",
    default=False,
    help="Do not wait for the long-running operation to finish.",
)

disable_public_ip = CLIArgumentType(
    validator=validators.validate_disable_public_ip,
    options_list=["--disable-public-ip"],
    type=str,
    help="Disable the deployment of a public IP address, load balancer, and network security group while testing a private endpoint.",
)


force = CLIArgumentType(
    options_list=["--force"],
    action="store_true",
    default=False,
    help="Force run the command. This will create the directory to download files if it does not exist.",
)
#

test_id = CLIArgumentType(
    validator=validators.validate_test_id,
    completer=completers.get_test_id_completion_list(),
    options_list=["--test-id", "-t"],
    type=str,
    help="Test ID of the load test",
)

test_id_no_completer = CLIArgumentType(
    validator=validators.validate_test_id,
    options_list=["--test-id", "-t"],
    type=str,
    help="Test ID of the load test",
)

test_run_id = CLIArgumentType(
    validator=validators.validate_test_run_id,
    completer=completers.get_test_run_id_completion_list(),
    options_list=["--test-run-id", "-r"],
    type=str,
    help="Test run ID of the load test run",
)

test_run_id_no_completer = CLIArgumentType(
    validator=validators.validate_test_run_id,
    options_list=["--test-run-id", "-r"],
    type=str,
    help="Test run ID of the load test run",
)

existing_test_run_id = CLIArgumentType(
    validator=validators.validate_test_run_id,
    completer=completers.get_test_run_id_completion_list(),
    options_list=["--existing-test-run-id"],
    type=str,
    help="Test run ID of an existing load test run which should be rerun.",
)

test_plan = CLIArgumentType(
    validator=validators.validate_test_plan_path,
    options_list=["--test-plan"],
    type=str,
    help="Reference to the test plan file. If `testType: JMX`: path to the JMeter script. If `testType: URL`: path to the requests JSON file. If `testType: Locust`: path to the Locust test script.",
)

test_type = CLIArgumentType(
    validator=validators.validate_test_type,
    options_list=["--test-type"],
    type=str,
    choices=utils.get_enum_values(models.AllowedTestTypes),
    help="Type of the load test.",
)

load_test_config_file = CLIArgumentType(
    validator=validators.validate_load_test_config_file,
    options_list=["--load-test-config-file"],
    type=str,
    help="Path to the load test config file. Refer https://learn.microsoft.com/azure/load-testing/reference-test-config-yaml.",
)

test_display_name = CLIArgumentType(
    options_list=["--display-name"],
    type=str,
    help="Display name of the load test.",
)

test_run_display_name = CLIArgumentType(
    options_list=["--display-name"],
    type=str,
    help="Display name of the load test run.",
)

engine_instances = CLIArgumentType(
    options_list=["--engine-instances"],
    type=int,
    help="Number of engine instances on which the test should run.",
)

key_vault_reference_identity = CLIArgumentType(
    validator=validators.validate_keyvault_identity_ref_id,
    options_list=["--keyvault-reference-id"],
    type=str,
    help="The identity that will be used to access the key vault.",
)

metrics_reference_identity = CLIArgumentType(
    validator=validators.validate_metrics_identity_ref_id,
    options_list=["--metrics-reference-id"],
    type=str,
    help="The identity that will be used to get the metrics of the configured apps from server pass-fail criteria.",
)

split_csv = CLIArgumentType(
    validator=validators.validate_split_csv,
    options_list=["--split-csv"],
    type=str,
    help="Split CSV files evenly among engine instances.",
)

subnet_id = CLIArgumentType(
    validator=validators.validate_subnet_id,
    options_list=["--subnet-id"],
    type=str,
    help="Resource ID of the subnet to use for private load test.",
)

test_description = CLIArgumentType(
    options_list=["--description"],
    type=str,
    help="Description of the load test.",
)

test_run_description = CLIArgumentType(
    options_list=["--description"],
    type=str,
    help="Description of the load test run.",
)

env = CLIArgumentType(
    validator=validators.validate_env_vars,
    options_list=["--env"],
    nargs="*",
    help="space-separated environment variables: key[=value] [key[=value] ...]. "
    + quote_text.format("environment variables"),
)

secret = CLIArgumentType(
    validator=validators.validate_secrets,
    options_list=["--secret"],
    nargs="*",
    help="space-separated secrets: key[=value] [key[=value] ...]. Secrets should be stored in Azure Key Vault, and the secret identifier should be provided as the value."
    + quote_text.format("secrets"),
)

certificate = CLIArgumentType(
    validator=validators.validate_certificate,
    options_list=["--certificate"],
    nargs="?",
    help="a single certificate in 'key[=value]' format. The certificate should be stored in Azure Key Vault in PFX format, and the certificate identifier should be provided as the value."
    + quote_text.format("certificate"),
)

test_run_debug_mode = CLIArgumentType(
    options_list=["--debug-mode"],
    action="store_true",
    default=False,
    help="Enable debug level logging for the test run.",
)

dir_path = CLIArgumentType(
    validator=validators.validate_dir_path,
    options_list=["--path"],
    type=str,
    help="Path of the directory to download files.",
)

file_name = CLIArgumentType(
    options_list=["--file-name"],
    type=str,
    help="Name of the file.",
)

file_path = CLIArgumentType(
    validator=validators.validate_file_path,
    options_list=["--path"],
    type=str,
    help="Path to the file to upload.",
)

file_type = CLIArgumentType(
    validator=validators.validate_file_type,
    completer=get_generic_completion_list(
        utils.get_enum_values(models.AllowedFileTypes)
    ),
    options_list=["--file-type"],
    type=str,
    help=f"Type of file to be uploaded. Allowed values: {', '.join(utils.get_enum_values(models.AllowedFileTypes))}. Ensure that the ZIP file remains below 50 MB in size. Only 5 ZIP artifacts are allowed with a maximum of 1000 files in each and uncompressed size of 1 GB",
)

test_run_input = CLIArgumentType(
    options_list=["--input"],
    action="store_true",
    default=False,
    help="Download the input files zip.",
)

test_run_log = CLIArgumentType(
    options_list=["--log"],
    action="store_true",
    default=False,
    help="Download the log files zip.",
)

test_run_results = CLIArgumentType(
    options_list=["--result"],
    action="store_true",
    default=False,
    help="Download the results files zip.",
)

test_run_report = CLIArgumentType(
    options_list=["--report"],
    action="store_true",
    default=False,
    help="Download the dashboard report files zip.",
)

app_component_id = CLIArgumentType(
    validator=validators.validate_app_component_id,
    options_list=["--app-component-id"],
    type=str,
    help="Fully qualified resource ID of the App Component. For example, subscriptions/{subId}/resourceGroups/{rg}/providers/Microsoft.LoadTestService/loadtests/{resName}",
)

app_component_name = CLIArgumentType(
    options_list=["--app-component-name"],
    type=str,
    help="Name of the app component. Refer https://learn.microsoft.com/cli/azure/resource#az-resource-show",
)

app_component_type = CLIArgumentType(
    validator=validators.validate_app_component_type,
    options_list=["--app-component-type"],
    type=str,
    help="Type of resource of the app component. Refer https://learn.microsoft.com/cli/azure/resource#az-resource-show",
)

app_component_kind = CLIArgumentType(
    options_list=["--app-component-kind"],
    type=str,
    help="Kind of the app component. Refer https://learn.microsoft.com/cli/azure/resource#az-resource-show",
)

server_metric_id = CLIArgumentType(
    validator=validators.validate_metric_id,
    options_list=["--metric-id"],
    type=str,
    help="Fully qualified ID of the server metric. Refer https://learn.microsoft.com/en-us/rest/api/monitor/metric-definitions/list#metricdefinition",
)

server_metric_name = CLIArgumentType(
    options_list=["--metric-name"],
    type=str,
    help="Name of the metric. Example, requests/duration",
)

server_metric_namespace = CLIArgumentType(
    options_list=["--metric-namespace"],
    type=str,
    help="Namespace of the server metric. Example, microsoft.insights/components",
)

server_metric_aggregation = CLIArgumentType(
    options_list=["--aggregation"],
    type=str,
    help="Aggregation to be applied on the metric.",
)

metric_name = CLIArgumentType(
    options_list=["--metric-name", "--metric-definition-name"],
    type=str,
    help="Name of the metric.",
)

metric_namespace = CLIArgumentType(
    validator=validators.validate_metric_namespaces,
    completer=get_generic_completion_list(
        utils.get_enum_values(models.AllowedMetricNamespaces)
    ),
    options_list=["--metric-namespace"],
    required=True,
    type=str,
    help=f"Namespace of the metric. Allowed values: {', '.join(utils.get_enum_values(models.AllowedMetricNamespaces))}",
)

metric_dimension = CLIArgumentType(
    options_list=["--metric-dimension"],
    type=str,
    help="Value of the metric dimension.",
)

start_iso_time = CLIArgumentType(
    validator=validators.validate_start_iso_time,
    options_list=["--start-time"],
    type=str,
    help="ISO 8601 formatted start time.",
)

end_iso_time = CLIArgumentType(
    validator=validators.validate_end_iso_time,
    options_list=["--end-time"],
    type=str,
    help="ISO 8601 formatted end time.",
)

interval = CLIArgumentType(
    validator=validators.validate_interval,
    completer=get_generic_completion_list(
        utils.get_enum_values(models.AllowedIntervals)
    ),
    options_list=["--interval"],
    type=str,
    help=f"ISO 8601 formatted interval. Allowed values: {', '.join(utils.get_enum_values(models.AllowedIntervals))}",
)

aggregation = CLIArgumentType(
    options_list=["--aggregation"],
    type=str,
    help="Operation used to aggregate the metrics",
)

dimension_filters = CLIArgumentType(
    validator=validators.validate_dimension_filters,
    options_list=["--dimension-filters"],
    nargs="*",
    help=(
        "space and comma-separated dimension filters: key1[=value1] key1[=value2] key2[=value3] format ...]. "
        "* is supported as a wildcard for both key and value. "
        "Example: `--dimension-filters key1=value1 key2=*`, `--dimension-filters *`"
    ),
)

autostop = CLIArgumentType(
    validator=validators.validate_autostop_enable_disable,
    options_list=["--autostop"],
    type=str,
    help="Whether auto-stop should be enabled or disabled. Allowed values are enable/disable.",
)

autostop_error_rate = CLIArgumentType(
    options_list=["--autostop-error-rate"],
    type=float,
    validator=validators.validate_autostop_error_rate,
    help="Threshold percentage of errors on which test run should be automatically stopped. Allowed values are in range of [0.0,100.0]",
)

autostop_error_rate_time_window = CLIArgumentType(
    options_list=["--autostop-time-window"],
    type=int,
    validator=validators.validate_autostop_error_rate_time_window,
    help="Time window during which the error percentage should be evaluated in seconds.",
)

regionwise_engines = CLIArgumentType(
    options_list=["--regionwise-engines"],
    validator=validators.validate_regionwise_engines,
    nargs="+",
    help="Specify the engine count for each region in the format: region1=engineCount1 region2=engineCount2 .... Use region names in the format accepted by Azure Resource Manager (ARM). Ensure the regions are supported by Azure Load Testing. Multi-region load tests can only target public endpoints.",
)

engine_ref_id_type = CLIArgumentType(
    options_list=["--engine-ref-id-type"],
    type=str,
    completer=get_generic_completion_list(
        utils.get_enum_values(models.EngineIdentityType)
    ),
    choices=utils.get_enum_values(models.EngineIdentityType),
    help="Type of identity to be configured for the engine.",
)

engine_ref_ids = CLIArgumentType(
    options_list=["--engine-ref-ids"],
    nargs="+",
    validator=validators.validate_engine_ref_ids,
    help="Space separated list of fully qualified resource IDs of the managed identities to be configured on the engine. Required only for user assigned identities. ",
)

response_time_aggregate = CLIArgumentType(
    options_list=["--aggregation"],
    type=str,
    choices=utils.get_enum_values(models.AllowedTrendsResponseTimeAggregations),
    help="Specify the aggregation method for response time.",
)

trigger_id = CLIArgumentType(
    validator=validators.validate_trigger_id,
    options_list=["--trigger-id"],
    type=str,
    help="Trigger ID of the load trigger",
)

trigger_start_date_time = CLIArgumentType(
    options_list=["--start-date-time"],
    type=trigger_utils.parse_datetime_in_utc,
    help="Start date time of the load trigger schedule",
)

recurrence_type = CLIArgumentType(
    options_list=["--recurrence-type"],
    type=str,
    choices=utils.get_enum_values(Frequency),
    help="Recurrence type of the load trigger schedule",
)

end_after_occurrences = CLIArgumentType(
    options_list=["--end-after-occurrence"],
    type=int,
    help="End after occurrence of the load trigger schedule",
)

end_after_date_time = CLIArgumentType(
    options_list=["--end-after-date-time"],
    type=trigger_utils.parse_datetime_in_utc,
    help="End after date time of the load trigger schedule",
)

test_ids = CLIArgumentType(
    options_list=["--test-ids"],
    nargs=1,
    validator=validators.validate_schedule_test_ids,
    help="Test IDs of the load tests to be triggered by schedule. Currently we only support one test ID per schedule.",
)

trigger_display_name = CLIArgumentType(
    options_list=["--display-name"],
    type=str,
    help="Display name of the load trigger schedule",
)

trigger_description = CLIArgumentType(
    options_list=["--description"],
    type=str,
    help="Description of the load trigger schedule",
)

recurrence_cron_expression = CLIArgumentType(
    options_list=["--recurrence-cron-exp"],
    type=str,
    help="Cron expression for the recurrence type 'Cron'.",
)

recurrence_interval = CLIArgumentType(
    options_list=["--recurrence-interval"],
    type=int,
    help="Interval for all recurrence type except 'Cron'.",
)

recurrence_dates_in_month = CLIArgumentType(
    options_list=["--recurrence-dates"],
    nargs="+",
    type=int,
    validator=validators.validate_recurrence_dates_in_month,
    help="Space separated list of dates in month for the recurrence type 'Monthly'.",
)

recurrence_week_days = CLIArgumentType(
    options_list=["--recurrence-week-days"],
    choices=utils.get_enum_values(WeekDays),
    nargs="*",
    help="Week days for the recurrence type 'Weekly' and 'MonthlyByDays'.",
)

recurrence_index = CLIArgumentType(
    options_list=["--recurrence-index"],
    type=int,
    choices=[1, 2, 3, 4, 5],
    help="Index for the recurrence type 'MonthlyByDays'.",
)

list_schedule_test_ids = CLIArgumentType(
    options_list=["--test-ids"],
    nargs="*",
    help="List all the schedules which are associated with the provided test ids.",
)

list_schedule_states = CLIArgumentType(
    options_list=["--states"],
    nargs="*",
    choices=utils.get_enum_values(TriggerState),
    help="List all the schedules in the resource which are in the provided states.",
)

notification_rule_test_ids = CLIArgumentType(
    options_list=["--test-ids"],
    nargs="+",
    validator=validators.validate_notification_rule_test_ids,
    help="Space separated list of test ids for the notification rule.",
)

notification_display_name = CLIArgumentType(
    option_list=["--display-name"],
    type=str,
    help="Display name of notification rule.",
)

notification_rule_id = CLIArgumentType(
    validator=validators.validate_notification_rule_id,
    options_list=["--notification-rule-id", "-i"],
    type=str,
    help="Identifier for the notification rule.",
)

action_groups = CLIArgumentType(
    option_list=["--action-groups"],
    nargs="*",
    help="Space separated list of resource ids of action groups for the notification rule.",
)

notification_rule_event = CLIArgumentType(
    option_list=["--event"],
    validator=validators.validate_event,
    nargs="+",
    action="append",
    help="Event to be enabled on the notification rule. Expected format is --event event-id='event id' type='event type' status='a list of statuses in comma-separated format' result='a list of results in comma-separated format'. Status and result fields are valid only for event type 'TestRunEnded'.",
)

notification_rule_remove_event = CLIArgumentType(
    option_list=["--remove-event"],
    nargs="+",
    validator=validators.validate_remove_event,
    action="append",
    help="Provide the event id of the event to be removed from the notification rule. Format should be --remove-event event-id='event id'.",
)

notification_rule_add_event = CLIArgumentType(
    option_list=["--add-event"],
    validator=validators.validate_add_event,
    nargs="+",
    action="append",
    help="Event to be enabled on the notification rule. Expected format is --event event-id='event id' type='event type' status='a list of statuses in comma-separated format' result='a list of results in comma-separated format'. Status and result fields are valid only for event type 'TestRunEnded'.",
)

notification_all_tests = CLIArgumentType(
    option_list=["--all-tests"],
    action="store_true",
    default=False,
    help="Provide this flag if all tests should be included for the notification rule. This will override any tests provided using --test-ids."
)

notification_all_events = CLIArgumentType(
    option_list=["--all-events"],
    action="store_true",
    default=False,
    help="Provide this flag if all events should be included for the notification rule. This will override any events provided using --event."
)
