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
"""Hermetic wiring tests for the real `Client` / `AsyncClient` constructors.

`BaseClient.__init__` builds the service container before any network I/O and
`grpc.insecure_channel` is lazy, so constructing the clients opens no connection.
The shared Keycloak provider factory is patched so the D18 config never triggers a
real ROPC login. These tests guard the `ServicesContainer` keyword wiring: a mismatch
between the constructor kwargs and the declared container fields raises `TypeError` at
build time.
"""
from unittest.mock import (
    MagicMock,
    patch,
)

from ondewo.survey.client.async_client import AsyncClient
from ondewo.survey.client.client import Client
from ondewo.survey.client.client_config import ClientConfig
from ondewo.survey.client.services.async_fhir import FHIR as AsyncFHIR
from ondewo.survey.client.services.async_survey import Survey as AsyncSurvey
from ondewo.survey.client.services.fhir import FHIR
from ondewo.survey.client.services.survey import Survey

# Patch targets for the shared-provider factory, resolved in each interface module's namespace.
_SYNC_FACTORY: str = 'ondewo.survey.client.services_interface.get_keycloak_token_provider'
_ASYNC_FACTORY: str = 'ondewo.survey.client.async_services_interface.get_keycloak_token_provider'

HOST: str = 'localhost'
PORT: str = '50051'
USERNAME: str = 'tech-user@example.com'
PASSWORD: str = 's3cr3t'
KEYCLOAK_URL: str = 'https://kc.example.com/auth'
REALM: str = 'ondewo-ccai-platform'
CLIENT_ID: str = 'ondewo-survey-cai-sdk-public'


def _make_config() -> ClientConfig:
    """Build a valid Keycloak-path `ClientConfig` for the wiring tests.

    Returns:
        ClientConfig:
            A config wired for the D18 Keycloak auth path.
    """
    return ClientConfig(
        host=HOST,
        port=PORT,
        user_name=USERNAME,
        password=PASSWORD,
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
    )


def test_client_wires_survey_and_fhir_services() -> None:
    """The real `Client` populates `services.survey`/`services.fhir` with the right types."""
    with patch(_SYNC_FACTORY, return_value=MagicMock(name='KeycloakTokenProvider')):
        client: Client = Client(config=_make_config(), use_secure_channel=False)

    assert isinstance(client.services.survey, Survey)
    assert isinstance(client.services.fhir, FHIR)


def test_async_client_wires_survey_and_fhir_services() -> None:
    """The real `AsyncClient` populates `services.survey`/`services.fhir` with the right types."""
    with patch(_ASYNC_FACTORY, return_value=MagicMock(name='KeycloakTokenProvider')):
        client: AsyncClient = AsyncClient(config=_make_config(), use_secure_channel=False)

    assert isinstance(client.services.survey, AsyncSurvey)
    assert isinstance(client.services.fhir, AsyncFHIR)
