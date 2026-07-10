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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.ces.v1beta',
    manifest={
        'ApplicationIntegrationTool',
    },
)


class ApplicationIntegrationTool(proto.Message):
    r"""A tool to support Application Integration calls.
    See
    https://cloud.google.com/application-integration/docs/overview
    for more details.

    Attributes:
        name (str):
            Optional. The application integration tool
            name.
        description (str):
            Optional. The tool description.
        integration_version (str):
            Required. The full name of the referenced Application
            Integration version. Format:
            ``projects/{project}/locations/{location}/integrations/{integration}/versions/{version}``
        trigger_id (str):
            Required. ID of integration's trigger to invoke. Format:
            ``api_trigger/{trigger_name}`` Reference:
            https://cloud.google.com/application-integration/docs/configure-api-trigger#configure-an-api-trigger
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    integration_version: str = proto.Field(
        proto.STRING,
        number=3,
    )
    trigger_id: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
