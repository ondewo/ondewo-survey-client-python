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

Configuration is read from ``examples/environment.env`` (loaded via python-dotenv,
relative to this file so the working directory does not matter). Copy your real
values into that file and run::

    python examples/survey_list_surveys_example.py
"""
import os
import sys
from pathlib import Path
from typing import (
    List,
    Sequence,
    Tuple,
)

import grpc
from dotenv import load_dotenv
from loguru import logger as log

from ondewo.survey.client.client import Client
from ondewo.survey.client.client_config import ClientConfig
from ondewo.survey.survey_pb2 import (
    ListSurveysRequest,
    ListSurveysResponse,
    Survey,
)
from ondewo.survey.utils.keycloak import get_keycloak_token_provider

# Load the example configuration relative to this script so cwd does not matter.
load_dotenv(Path(__file__).with_name('environment.env'))


def build_client_config() -> ClientConfig:
    """
    Build a `ClientConfig` for the Keycloak offline-token auth path from the environment.

    Reads the canonical env vars (see ``examples/environment.env``); each lookup falls
    back to a non-secret local-development default when the variable is unset or blank.

    Returns:
        ClientConfig:
            A config wired for the D18 Keycloak headless auth path.
    """
    return ClientConfig(
        host=os.getenv('ONDEWO_HOST') or 'localhost',
        port=os.getenv('ONDEWO_PORT') or '50051',
        user_name=os.getenv('KEYCLOAK_USER_NAME') or 'tech-user@ondewo.com',
        password=os.getenv('KEYCLOAK_PASSWORD') or 'change-me',
        keycloak_url=os.getenv('KEYCLOAK_URL') or 'https://my-host/auth',
        realm=os.getenv('KEYCLOAK_REALM') or 'ondewo-ccai-platform',
        client_id=os.getenv('KEYCLOAK_CLIENT_ID') or 'ondewo-survey-cai-sdk-public',
        keycloak_verify_ssl=(os.getenv('KEYCLOAK_VERIFY_SSL', 'true').lower() == 'true'),
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

    Raises:
        grpc.RpcError:
            If the `ListSurveys` RPC fails; the status code and details are logged.
    """
    log.info('START: list_surveys: ListSurveys')
    metadata: Sequence[Tuple[str, str]] = get_keycloak_token_provider(config).bearer_metadata()
    request: ListSurveysRequest = ListSurveysRequest(page_token='page_size-10000')
    try:
        response: ListSurveysResponse = client.services.survey.stub.ListSurveys(request=request, metadata=metadata)
    except grpc.RpcError as rpc_error:
        log.error(f'ListSurveys RPC failed: code={rpc_error.code()} details={rpc_error.details()}')
        raise
    surveys: List[Survey] = list(response.surveys)
    log.info(f'DONE: list_surveys: ListSurveys. Retrieved {len(surveys)} survey(s)')
    return surveys


def main() -> None:
    """
    Connect to the SURVEY server, list the surveys, and print a short summary.
    """
    config: ClientConfig = build_client_config()
    use_secure_channel: bool = os.getenv('ONDEWO_USE_SECURE_CHANNEL', 'false').lower() == 'true'
    log.info(f'START: main: connecting to {config.host}:{config.port} (secure={use_secure_channel})')
    client: Client = Client(config=config, use_secure_channel=use_secure_channel)
    try:
        surveys: List[Survey] = list_surveys(client=client, config=config)
        print(f'Retrieved {len(surveys)} survey(s):')
        for survey in surveys:
            print(f'  - {survey.survey_id}: {survey.display_name} [{survey.language_code}]')
    finally:
        client.disconnect()
        log.info('DONE: main: client disconnected')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        log.exception('survey_list_surveys_example failed')
        sys.exit(1)
