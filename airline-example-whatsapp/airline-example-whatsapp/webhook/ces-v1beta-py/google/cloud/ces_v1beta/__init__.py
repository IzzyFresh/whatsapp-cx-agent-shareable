# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.cloud.ces_v1beta import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata


from .services.agent_service import AgentServiceClient
from .services.agent_service import AgentServiceAsyncClient
from .services.evaluation_service import EvaluationServiceClient
from .services.evaluation_service import EvaluationServiceAsyncClient
from .services.session_service import SessionServiceClient
from .services.session_service import SessionServiceAsyncClient
from .services.tool_service import ToolServiceClient
from .services.tool_service import ToolServiceAsyncClient

from .types.agent import Agent
from .types.agent_service import BatchDeleteConversationsRequest
from .types.agent_service import BatchDeleteConversationsResponse
from .types.agent_service import CreateAgentRequest
from .types.agent_service import CreateAppRequest
from .types.agent_service import CreateAppVersionRequest
from .types.agent_service import CreateDeploymentRequest
from .types.agent_service import CreateExampleRequest
from .types.agent_service import CreateGuardrailRequest
from .types.agent_service import CreateToolRequest
from .types.agent_service import CreateToolsetRequest
from .types.agent_service import DeleteAgentRequest
from .types.agent_service import DeleteAppRequest
from .types.agent_service import DeleteAppVersionRequest
from .types.agent_service import DeleteConversationRequest
from .types.agent_service import DeleteDeploymentRequest
from .types.agent_service import DeleteExampleRequest
from .types.agent_service import DeleteGuardrailRequest
from .types.agent_service import DeleteToolRequest
from .types.agent_service import DeleteToolsetRequest
from .types.agent_service import ExportAppRequest
from .types.agent_service import ExportAppResponse
from .types.agent_service import GenerateAppResourceResponse
from .types.agent_service import GetAgentRequest
from .types.agent_service import GetAppRequest
from .types.agent_service import GetAppVersionRequest
from .types.agent_service import GetChangelogRequest
from .types.agent_service import GetConversationRequest
from .types.agent_service import GetDeploymentRequest
from .types.agent_service import GetExampleRequest
from .types.agent_service import GetGuardrailRequest
from .types.agent_service import GetToolRequest
from .types.agent_service import GetToolsetRequest
from .types.agent_service import ImportAppRequest
from .types.agent_service import ImportAppResponse
from .types.agent_service import ListAgentsRequest
from .types.agent_service import ListAgentsResponse
from .types.agent_service import ListAppsRequest
from .types.agent_service import ListAppsResponse
from .types.agent_service import ListAppVersionsRequest
from .types.agent_service import ListAppVersionsResponse
from .types.agent_service import ListChangelogsRequest
from .types.agent_service import ListChangelogsResponse
from .types.agent_service import ListConversationsRequest
from .types.agent_service import ListConversationsResponse
from .types.agent_service import ListDeploymentsRequest
from .types.agent_service import ListDeploymentsResponse
from .types.agent_service import ListExamplesRequest
from .types.agent_service import ListExamplesResponse
from .types.agent_service import ListGuardrailsRequest
from .types.agent_service import ListGuardrailsResponse
from .types.agent_service import ListToolsetsRequest
from .types.agent_service import ListToolsetsResponse
from .types.agent_service import ListToolsRequest
from .types.agent_service import ListToolsResponse
from .types.agent_service import OperationMetadata
from .types.agent_service import RestoreAppVersionRequest
from .types.agent_service import RestoreAppVersionResponse
from .types.agent_service import UpdateAgentRequest
from .types.agent_service import UpdateAppRequest
from .types.agent_service import UpdateDeploymentRequest
from .types.agent_service import UpdateExampleRequest
from .types.agent_service import UpdateGuardrailRequest
from .types.agent_service import UpdateToolRequest
from .types.agent_service import UpdateToolsetRequest
from .types.app import AmbientSoundConfig
from .types.app import App
from .types.app import AudioProcessingConfig
from .types.app import AudioRecordingConfig
from .types.app import BargeInConfig
from .types.app import ClientCertificateSettings
from .types.app import CloudLoggingSettings
from .types.app import ConversationLoggingSettings
from .types.app import DataStoreSettings
from .types.app import EvaluationMetricsThresholds
from .types.app import EvaluationPersona
from .types.app import EvaluationSettings
from .types.app import LanguageSettings
from .types.app import LoggingSettings
from .types.app import RedactionConfig
from .types.app import SynthesizeSpeechConfig
from .types.app import TimeZoneSettings
from .types.app_version import AppSnapshot
from .types.app_version import AppVersion
from .types.application_integration_tool import ApplicationIntegrationTool
from .types.auth import ApiAuthentication
from .types.auth import ApiKeyConfig
from .types.auth import BearerTokenConfig
from .types.auth import EndUserAuthConfig
from .types.auth import OAuthConfig
from .types.auth import ServiceAccountAuthConfig
from .types.auth import ServiceAgentIdTokenAuthConfig
from .types.bigquery_export import BigQueryExportSettings
from .types.changelog import Changelog
from .types.client_function import ClientFunction
from .types.common import Callback
from .types.common import ChannelProfile
from .types.common import ModelSettings
from .types.common import ServiceDirectoryConfig
from .types.common import Span
from .types.common import TlsConfig
from .types.common import TriggerAction
from .types.common import ExecutionType
from .types.connector_tool import Action
from .types.connector_tool import ConnectorTool
from .types.connector_toolset import ConnectorToolset
from .types.conversation import Conversation
from .types.data_store import DataStore
from .types.data_store_tool import DataStoreTool
from .types.deployment import Deployment
from .types.evaluation import AggregatedMetrics
from .types.evaluation import Evaluation
from .types.evaluation import EvaluationConfig
from .types.evaluation import EvaluationDataset
from .types.evaluation import EvaluationErrorInfo
from .types.evaluation import EvaluationExpectation
from .types.evaluation import EvaluationResult
from .types.evaluation import EvaluationRun
from .types.evaluation import OptimizationConfig
from .types.evaluation import PersonaRunConfig
from .types.evaluation import RunEvaluationRequest
from .types.evaluation import ScheduledEvaluationRun
from .types.evaluation import GoldenRunMethod
from .types.evaluation_service import CreateEvaluationDatasetRequest
from .types.evaluation_service import CreateEvaluationExpectationRequest
from .types.evaluation_service import CreateEvaluationRequest
from .types.evaluation_service import CreateScheduledEvaluationRunRequest
from .types.evaluation_service import DeleteEvaluationDatasetRequest
from .types.evaluation_service import DeleteEvaluationExpectationRequest
from .types.evaluation_service import DeleteEvaluationRequest
from .types.evaluation_service import DeleteEvaluationResultRequest
from .types.evaluation_service import DeleteEvaluationRunOperationMetadata
from .types.evaluation_service import DeleteEvaluationRunRequest
from .types.evaluation_service import DeleteScheduledEvaluationRunRequest
from .types.evaluation_service import GenerateEvaluationOperationMetadata
from .types.evaluation_service import GenerateEvaluationRequest
from .types.evaluation_service import GetEvaluationDatasetRequest
from .types.evaluation_service import GetEvaluationExpectationRequest
from .types.evaluation_service import GetEvaluationRequest
from .types.evaluation_service import GetEvaluationResultRequest
from .types.evaluation_service import GetEvaluationRunRequest
from .types.evaluation_service import GetScheduledEvaluationRunRequest
from .types.evaluation_service import ImportEvaluationsOperationMetadata
from .types.evaluation_service import ImportEvaluationsRequest
from .types.evaluation_service import ImportEvaluationsResponse
from .types.evaluation_service import ListEvaluationDatasetsRequest
from .types.evaluation_service import ListEvaluationDatasetsResponse
from .types.evaluation_service import ListEvaluationExpectationsRequest
from .types.evaluation_service import ListEvaluationExpectationsResponse
from .types.evaluation_service import ListEvaluationResultsRequest
from .types.evaluation_service import ListEvaluationResultsResponse
from .types.evaluation_service import ListEvaluationRunsRequest
from .types.evaluation_service import ListEvaluationRunsResponse
from .types.evaluation_service import ListEvaluationsRequest
from .types.evaluation_service import ListEvaluationsResponse
from .types.evaluation_service import ListScheduledEvaluationRunsRequest
from .types.evaluation_service import ListScheduledEvaluationRunsResponse
from .types.evaluation_service import RunEvaluationOperationMetadata
from .types.evaluation_service import RunEvaluationResponse
from .types.evaluation_service import TestPersonaVoiceRequest
from .types.evaluation_service import TestPersonaVoiceResponse
from .types.evaluation_service import UpdateEvaluationDatasetRequest
from .types.evaluation_service import UpdateEvaluationExpectationRequest
from .types.evaluation_service import UpdateEvaluationRequest
from .types.evaluation_service import UpdateScheduledEvaluationRunRequest
from .types.example import AgentTransfer
from .types.example import Blob
from .types.example import Chunk
from .types.example import Example
from .types.example import Image
from .types.example import Message
from .types.example import ToolCall
from .types.example import ToolResponse
from .types.file_search_tool import FileSearchTool
from .types.google_search_tool import GoogleSearchTool
from .types.guardrail import Guardrail
from .types.mcp_tool import McpTool
from .types.mcp_toolset import McpToolset
from .types.omnichannel import Omnichannel
from .types.omnichannel import OmnichannelIntegrationConfig
from .types.omnichannel_service import OmnichannelOperationMetadata
from .types.open_api_tool import OpenApiTool
from .types.open_api_toolset import OpenApiToolset
from .types.python_function import PythonFunction
from .types.schema import Schema
from .types.search_suggestions import GoogleSearchSuggestions
from .types.search_suggestions import WebSearchQuery
from .types.session_service import BidiSessionClientMessage
from .types.session_service import BidiSessionServerMessage
from .types.session_service import Citations
from .types.session_service import EndSession
from .types.session_service import Event
from .types.session_service import GoAway
from .types.session_service import InputAudioConfig
from .types.session_service import InterruptionSignal
from .types.session_service import OutputAudioConfig
from .types.session_service import RecognitionResult
from .types.session_service import RunSessionRequest
from .types.session_service import RunSessionResponse
from .types.session_service import SessionConfig
from .types.session_service import SessionInput
from .types.session_service import SessionOutput
from .types.session_service import ToolCalls
from .types.session_service import ToolResponses
from .types.session_service import AudioEncoding
from .types.system_tool import SystemTool
from .types.tool import Tool
from .types.tool_predicate import ToolPredicate
from .types.tool_service import ExecuteToolRequest
from .types.tool_service import ExecuteToolResponse
from .types.tool_service import RetrieveToolSchemaRequest
from .types.tool_service import RetrieveToolSchemaResponse
from .types.tool_service import RetrieveToolsRequest
from .types.tool_service import RetrieveToolsResponse
from .types.toolset import Toolset
from .types.toolset_tool import ToolsetTool
from .types.vertex_ai_rag_retrieval_tool import VertexAiRagRetrievalTool

if hasattr(api_core, "check_python_version") and hasattr(api_core, "check_dependency_versions"):   # pragma: NO COVER
    api_core.check_python_version("google.cloud.ces_v1beta") # type: ignore
    api_core.check_dependency_versions("google.cloud.ces_v1beta") # type: ignore
else:   # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings
        import sys

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.ces_v1beta"
        if sys.version_info < (3, 9):
            warnings.warn("You are using a non-supported Python version " +
                          f"({_py_version_str}).  Google will not post any further " +
                          f"updates to {_package_label} supporting this Python version. " +
                          "Please upgrade to the latest Python version, or at " +
                          f"least to Python 3.9, and then update {_package_label}.",
                          FutureWarning)
        if sys.version_info[:2] == (3, 9):
            warnings.warn(f"You are using a Python version ({_py_version_str}) " +
                          f"which Google will stop supporting in {_package_label} in " +
                          "January 2026. Please " +
                          "upgrade to the latest Python version, or at " +
                          "least to Python 3.10, before then, and " +
                          f"then update {_package_label}.",
                          FutureWarning)

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(f"Package {_package_label} depends on " +
                          f"{_dependency_package}, currently installed at version " +
                          f"{_version_used_string}. Future updates to " +
                          f"{_package_label} will require {_dependency_package} at " +
                          f"version {_next_supported_version} or higher{_recommendation}." +
                          " Please ensure " +
                          "that either (a) your Python environment doesn't pin the " +
                          f"version of {_dependency_package}, so that updates to " +
                          f"{_package_label} can require the higher version, or " +
                          "(b) you manually update your Python environment to use at " +
                          f"least version {_next_supported_version} of " +
                          f"{_dependency_package}.",
                          FutureWarning)
    except Exception:
            warnings.warn("Could not determine the version of Python " +
                          "currently being used. To continue receiving " +
                          "updates for {_package_label}, ensure you are " +
                          "using a supported version of Python; see " +
                          "https://devguide.python.org/versions/")

__all__ = (
    'AgentServiceAsyncClient',
    'EvaluationServiceAsyncClient',
    'SessionServiceAsyncClient',
    'ToolServiceAsyncClient',
'Action',
'Agent',
'AgentServiceClient',
'AgentTransfer',
'AggregatedMetrics',
'AmbientSoundConfig',
'ApiAuthentication',
'ApiKeyConfig',
'App',
'AppSnapshot',
'AppVersion',
'ApplicationIntegrationTool',
'AudioEncoding',
'AudioProcessingConfig',
'AudioRecordingConfig',
'BargeInConfig',
'BatchDeleteConversationsRequest',
'BatchDeleteConversationsResponse',
'BearerTokenConfig',
'BidiSessionClientMessage',
'BidiSessionServerMessage',
'BigQueryExportSettings',
'Blob',
'Callback',
'Changelog',
'ChannelProfile',
'Chunk',
'Citations',
'ClientCertificateSettings',
'ClientFunction',
'CloudLoggingSettings',
'ConnectorTool',
'ConnectorToolset',
'Conversation',
'ConversationLoggingSettings',
'CreateAgentRequest',
'CreateAppRequest',
'CreateAppVersionRequest',
'CreateDeploymentRequest',
'CreateEvaluationDatasetRequest',
'CreateEvaluationExpectationRequest',
'CreateEvaluationRequest',
'CreateExampleRequest',
'CreateGuardrailRequest',
'CreateScheduledEvaluationRunRequest',
'CreateToolRequest',
'CreateToolsetRequest',
'DataStore',
'DataStoreSettings',
'DataStoreTool',
'DeleteAgentRequest',
'DeleteAppRequest',
'DeleteAppVersionRequest',
'DeleteConversationRequest',
'DeleteDeploymentRequest',
'DeleteEvaluationDatasetRequest',
'DeleteEvaluationExpectationRequest',
'DeleteEvaluationRequest',
'DeleteEvaluationResultRequest',
'DeleteEvaluationRunOperationMetadata',
'DeleteEvaluationRunRequest',
'DeleteExampleRequest',
'DeleteGuardrailRequest',
'DeleteScheduledEvaluationRunRequest',
'DeleteToolRequest',
'DeleteToolsetRequest',
'Deployment',
'EndSession',
'EndUserAuthConfig',
'Evaluation',
'EvaluationConfig',
'EvaluationDataset',
'EvaluationErrorInfo',
'EvaluationExpectation',
'EvaluationMetricsThresholds',
'EvaluationPersona',
'EvaluationResult',
'EvaluationRun',
'EvaluationServiceClient',
'EvaluationSettings',
'Event',
'Example',
'ExecuteToolRequest',
'ExecuteToolResponse',
'ExecutionType',
'ExportAppRequest',
'ExportAppResponse',
'FileSearchTool',
'GenerateAppResourceResponse',
'GenerateEvaluationOperationMetadata',
'GenerateEvaluationRequest',
'GetAgentRequest',
'GetAppRequest',
'GetAppVersionRequest',
'GetChangelogRequest',
'GetConversationRequest',
'GetDeploymentRequest',
'GetEvaluationDatasetRequest',
'GetEvaluationExpectationRequest',
'GetEvaluationRequest',
'GetEvaluationResultRequest',
'GetEvaluationRunRequest',
'GetExampleRequest',
'GetGuardrailRequest',
'GetScheduledEvaluationRunRequest',
'GetToolRequest',
'GetToolsetRequest',
'GoAway',
'GoldenRunMethod',
'GoogleSearchSuggestions',
'GoogleSearchTool',
'Guardrail',
'Image',
'ImportAppRequest',
'ImportAppResponse',
'ImportEvaluationsOperationMetadata',
'ImportEvaluationsRequest',
'ImportEvaluationsResponse',
'InputAudioConfig',
'InterruptionSignal',
'LanguageSettings',
'ListAgentsRequest',
'ListAgentsResponse',
'ListAppVersionsRequest',
'ListAppVersionsResponse',
'ListAppsRequest',
'ListAppsResponse',
'ListChangelogsRequest',
'ListChangelogsResponse',
'ListConversationsRequest',
'ListConversationsResponse',
'ListDeploymentsRequest',
'ListDeploymentsResponse',
'ListEvaluationDatasetsRequest',
'ListEvaluationDatasetsResponse',
'ListEvaluationExpectationsRequest',
'ListEvaluationExpectationsResponse',
'ListEvaluationResultsRequest',
'ListEvaluationResultsResponse',
'ListEvaluationRunsRequest',
'ListEvaluationRunsResponse',
'ListEvaluationsRequest',
'ListEvaluationsResponse',
'ListExamplesRequest',
'ListExamplesResponse',
'ListGuardrailsRequest',
'ListGuardrailsResponse',
'ListScheduledEvaluationRunsRequest',
'ListScheduledEvaluationRunsResponse',
'ListToolsRequest',
'ListToolsResponse',
'ListToolsetsRequest',
'ListToolsetsResponse',
'LoggingSettings',
'McpTool',
'McpToolset',
'Message',
'ModelSettings',
'OAuthConfig',
'Omnichannel',
'OmnichannelIntegrationConfig',
'OmnichannelOperationMetadata',
'OpenApiTool',
'OpenApiToolset',
'OperationMetadata',
'OptimizationConfig',
'OutputAudioConfig',
'PersonaRunConfig',
'PythonFunction',
'RecognitionResult',
'RedactionConfig',
'RestoreAppVersionRequest',
'RestoreAppVersionResponse',
'RetrieveToolSchemaRequest',
'RetrieveToolSchemaResponse',
'RetrieveToolsRequest',
'RetrieveToolsResponse',
'RunEvaluationOperationMetadata',
'RunEvaluationRequest',
'RunEvaluationResponse',
'RunSessionRequest',
'RunSessionResponse',
'ScheduledEvaluationRun',
'Schema',
'ServiceAccountAuthConfig',
'ServiceAgentIdTokenAuthConfig',
'ServiceDirectoryConfig',
'SessionConfig',
'SessionInput',
'SessionOutput',
'SessionServiceClient',
'Span',
'SynthesizeSpeechConfig',
'SystemTool',
'TestPersonaVoiceRequest',
'TestPersonaVoiceResponse',
'TimeZoneSettings',
'TlsConfig',
'Tool',
'ToolCall',
'ToolCalls',
'ToolPredicate',
'ToolResponse',
'ToolResponses',
'ToolServiceClient',
'Toolset',
'ToolsetTool',
'TriggerAction',
'UpdateAgentRequest',
'UpdateAppRequest',
'UpdateDeploymentRequest',
'UpdateEvaluationDatasetRequest',
'UpdateEvaluationExpectationRequest',
'UpdateEvaluationRequest',
'UpdateExampleRequest',
'UpdateGuardrailRequest',
'UpdateScheduledEvaluationRunRequest',
'UpdateToolRequest',
'UpdateToolsetRequest',
'VertexAiRagRetrievalTool',
'WebSearchQuery',
)
