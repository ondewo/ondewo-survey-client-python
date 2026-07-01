# Copyright 2021-2025 ONDEWO GmbH
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
"""
Minimal example: list the surveys on an ONDEWO SURVEY server.

This example shows the current, idiomatic way to talk to the SURVEY gRPC API:

1. Build a :class:`ClientConfig` for the Keycloak headless offline-token auth path
   (D18) — `keycloak_url`, `realm`, `client_id`, `user_name`, and `password`.
2. Construct the :class:`Client`, which wires up the `survey` service stub.
3. Acquire the shared :class:`KeycloakTokenProvider` for the config and attach its
   ``Authorization: Bearer`` metadata to the RPC call.
4. Call a representative RPC (``ListSurveys``) and handle the response.

Run it against a real server by exporting the connection/credentials env vars and
executing the file directly::

    export ONDEWO_SURVEY_HOST=127.0.0.1
    export ONDEWO_SURVEY_PORT=50051
    export ONDEWO_SURVEY_USER_NAME=tech-user@ondewo.com
    export ONDEWO_SURVEY_PASSWORD=...
    export ONDEWO_SURVEY_KEYCLOAK_URL=https://my-host/auth
    export ONDEWO_SURVEY_KEYCLOAK_REALM=ondewo-ccai-platform
    export ONDEWO_SURVEY_KEYCLOAK_CLIENT_ID=ondewo-survey-cai-sdk-public

    python examples/survey_list_surveys_example.py
"""
import os
from typing import (
    List,
    Sequence,
    Tuple,
)

from ondewo.survey.client.client import Client
from ondewo.survey.client.client_config import ClientConfig
from ondewo.survey.survey_pb2 import (
    ListSurveysRequest,
    ListSurveysResponse,
    Survey,
)
from ondewo.survey.utils.keycloak import get_keycloak_token_provider


def build_client_config() -> ClientConfig:
    """
    Build a `ClientConfig` for the Keycloak offline-token auth path from the environment.

    Returns:
        ClientConfig:
            A config wired for the D18 Keycloak headless auth path (falls back to
            sensible local-development defaults when the env vars are unset).
    """
    return ClientConfig(
        host=os.getenv('ONDEWO_SURVEY_HOST', 'localhost'),
        port=os.getenv('ONDEWO_SURVEY_PORT', '50051'),
        user_name=os.getenv('ONDEWO_SURVEY_USER_NAME', 'tech-user@ondewo.com'),
        password=os.getenv('ONDEWO_SURVEY_PASSWORD', 'change-me'),
        keycloak_url=os.getenv('ONDEWO_SURVEY_KEYCLOAK_URL', 'https://my-host/auth'),
        realm=os.getenv('ONDEWO_SURVEY_KEYCLOAK_REALM', 'ondewo-ccai-platform'),
        client_id=os.getenv('ONDEWO_SURVEY_KEYCLOAK_CLIENT_ID', 'ondewo-survey-cai-sdk-public'),
    )


def list_surveys(client: Client, config: ClientConfig) -> List[Survey]:
    """
    Call the `ListSurveys` RPC and return the surveys it yields.

    The Keycloak token provider is shared per config, so acquiring it here reuses the
    single ROPC login performed on first use and reads the auto-refreshed access token.

    Args:
        client (Client):
            A connected SURVEY client exposing the `survey` service stub.
        config (ClientConfig):
            The config the `client` was built from; used to look up the shared
            Keycloak token provider that supplies the bearer metadata.

    Returns:
        List[Survey]:
            The surveys returned by the server (may be empty).
    """
    metadata: Sequence[Tuple[str, str]] = get_keycloak_token_provider(config).bearer_metadata()
    request: ListSurveysRequest = ListSurveysRequest(page_token='page_size-10000')
    response: ListSurveysResponse = client.services.survey.stub.ListSurveys(request=request, metadata=metadata)
    return list(response.surveys)


def main() -> None:
    """
    Connect to the SURVEY server, list the surveys, and print a short summary.
    """
    config: ClientConfig = build_client_config()
    client: Client = Client(config=config, use_secure_channel=False)
    try:
        surveys: List[Survey] = list_surveys(client=client, config=config)
        print(f'Retrieved {len(surveys)} survey(s):')
        for survey in surveys:
            print(f'  - {survey.survey_id}: {survey.display_name} [{survey.language_code}]')
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
