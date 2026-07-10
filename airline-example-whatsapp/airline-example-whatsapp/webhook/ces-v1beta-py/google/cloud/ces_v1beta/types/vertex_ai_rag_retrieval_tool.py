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
        'VertexAiRagRetrievalTool',
    },
)


class VertexAiRagRetrievalTool(proto.Message):
    r"""A retrieval tool that uses Vertex AI RAG (Retrieval-Augmented
    Generation) to retrieve data.
    See
    http://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview
    for more details.

    Attributes:
        name (str):
            Identifier. The vertex AI RAG retrieval tool
            name.
        description (str):
            Required. The tool description.
        rag_resources (MutableSequence[google.cloud.ces_v1beta.types.VertexAiRagRetrievalTool.RagResource]):
            Optional. The list of rag resources to
            retrieve from.
        similarity_top_k (int):
            Optional. The similarity top k.
        vector_distance_threshold (float):
            Optional. The vector distance threshold.
    """

    class RagResource(proto.Message):
        r"""The definition of the Rag resource.

        Attributes:
            rag_corpus (str):
                Required. RagCorpora resource name. Format:
                ``projects/{project}/locations/{location}/ragCorpora/{rag_corpus}``
            rag_file_ids (MutableSequence[str]):
                Optional. List of RAG file IDs. The files should be in the
                same ``rag_corpus``.
        """

        rag_corpus: str = proto.Field(
            proto.STRING,
            number=1,
        )
        rag_file_ids: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=2,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    description: str = proto.Field(
        proto.STRING,
        number=2,
    )
    rag_resources: MutableSequence[RagResource] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=RagResource,
    )
    similarity_top_k: int = proto.Field(
        proto.INT32,
        number=4,
    )
    vector_distance_threshold: float = proto.Field(
        proto.FLOAT,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
