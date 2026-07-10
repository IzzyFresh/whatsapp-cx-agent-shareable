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
        'GoogleSearchTool',
    },
)


class GoogleSearchTool(proto.Message):
    r"""Represents a tool to perform Google web searches for
    grounding. See
    https://cloud.google.com/customer-engagement-ai/conversational-agents/ps/tool#google-search.

    Attributes:
        name (str):
            Required. The name of the tool.
        description (str):
            Optional. Description of the tool's purpose.
        context_urls (MutableSequence[str]):
            Optional. Content will be fetched directly
            from these URLs for context and grounding. More
            details:

            https://cloud.google.com/vertex-ai/generative-ai/docs/url-context.
            Example:

            "https://example.com/path.html". A maximum of 20
            URLs are allowed.
        preferred_domains (MutableSequence[str]):
            Optional. Specifies domain names to guide the
            search. The model will be instructed to
            prioritize these domains when formulating
            queries for google search. This is a best-effort
            hint and these domains may or may not be
            exclusively reflected in the final search
            results. Example: "example.com", "another.site".
            A maximum of 20 domains can be specified.
        exclude_domains (MutableSequence[str]):
            Optional. List of domains to be excluded from
            the search results. Example: "example.com".
            A maximum of 2000 domains can be excluded.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    context_urls: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    preferred_domains: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    exclude_domains: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
