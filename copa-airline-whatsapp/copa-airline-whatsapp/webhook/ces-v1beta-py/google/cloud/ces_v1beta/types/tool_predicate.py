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

from google.cloud.ces_v1beta.types import connector_tool


__protobuf__ = proto.module(
    package='google.cloud.ces.v1beta',
    manifest={
        'ToolPredicate',
    },
)


class ToolPredicate(proto.Message):
    r"""A predicate to match a tool created by a toolset.
    WILL BE DEPRECATED SOON.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        mcp_tool_predicate (google.cloud.ces_v1beta.types.ToolPredicate.McpToolPredicate):
            Optional. A tool predicate that is used to
            match a MCP tool.

            This field is a member of `oneof`_ ``tool_predicate``.
        open_api_tool_predicate (google.cloud.ces_v1beta.types.ToolPredicate.OpenApiToolPredicate):
            Optional. A tool predicate that is used to
            match an OpenAPI tool.

            This field is a member of `oneof`_ ``tool_predicate``.
        connector_tool_predicate (google.cloud.ces_v1beta.types.ToolPredicate.ConnectorToolPredicate):
            Optional. A tool predicate that is used to
            match a Connector tool.

            This field is a member of `oneof`_ ``tool_predicate``.
        display_name (str):
            Output only. The display name of the tool
            predicate and matches the tool predicate set.
    """

    class McpToolPredicate(proto.Message):
        r"""A tool predicate that is used to match a MCP tool.

        Attributes:
            tool_name (str):
                Required. The name of the individual tool in
                the MCP toolset.
        """

        tool_name: str = proto.Field(
            proto.STRING,
            number=1,
        )

    class OpenApiToolPredicate(proto.Message):
        r"""A tool predicate that is used to match an OpenAPI tool. If
        ``operation_id`` is specified, OpenAPI tools with the matching
        operation ID would be selected. Otherwise, OpenAPI tools with the
        matching ``path`` and ``method`` would be returned.

        Attributes:
            operation_id (str):
                Optional. The operationId field of the
                OpenAPI endpoint.
            path (str):
                Optional. The path of the OpenAPI endpoint.
            method (str):
                Optional. The HTTP method of the given path.
        """

        operation_id: str = proto.Field(
            proto.STRING,
            number=1,
        )
        path: str = proto.Field(
            proto.STRING,
            number=2,
        )
        method: str = proto.Field(
            proto.STRING,
            number=3,
        )

    class ConnectorToolPredicate(proto.Message):
        r"""A tool predicate that is used to match a Connector tool. The
        specified actions must match exactly one tool from the toolset.

        Attributes:
            action (google.cloud.ces_v1beta.types.Action):
                The connector operation to match.
        """

        action: connector_tool.Action = proto.Field(
            proto.MESSAGE,
            number=1,
            message=connector_tool.Action,
        )

    mcp_tool_predicate: McpToolPredicate = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof='tool_predicate',
        message=McpToolPredicate,
    )
    open_api_tool_predicate: OpenApiToolPredicate = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof='tool_predicate',
        message=OpenApiToolPredicate,
    )
    connector_tool_predicate: ConnectorToolPredicate = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof='tool_predicate',
        message=ConnectorToolPredicate,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
