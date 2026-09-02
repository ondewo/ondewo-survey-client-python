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
BOTH interface modules' provider factories are patched so the D18 config never triggers a
real ROPC login: `Client` resolves its provider through
`services_interface.get_keycloak_token_provider` and `AsyncClient` through the
`async_services_interface` one. Patching only one is a real hazard, not belt-and-braces: while
the async wrappers were regenerated onto the SYNCHRONOUS `ServicesInterface`, patching only
`_ASYNC_FACTORY` intercepted nothing and the constructor performed a real ROPC login against
the placeholder `kc.example.com`, which is what turned the `tests` workflow red on master. A
wiring test must not depend on which interface the client happens to route through, so it
patches both.

These tests guard the `ServicesContainer` keyword wiring: a mismatch
between the constructor kwargs and the declared container fields raises `TypeError` at
build time. They also guard the sync/async split itself, which `make create_async_services`
has silently collapsed twice.
"""

from unittest.mock import (
    MagicMock,
    patch,
)

import grpc

from ondewo.survey.client.async_client import AsyncClient
from ondewo.survey.client.async_services_interface import AsyncServicesInterface
from ondewo.survey.client.client import Client
from ondewo.survey.client.client_config import ClientConfig
from ondewo.survey.client.services.async_fhir import FHIR as AsyncFHIR
from ondewo.survey.client.services.async_survey import Survey as AsyncSurvey
from ondewo.survey.client.services.fhir import FHIR
from ondewo.survey.client.services.survey import Survey
from ondewo.survey.client.services_interface import ServicesInterface

# Patch targets for the shared-provider factory, resolved in each interface module's namespace.
_SYNC_FACTORY: str = "ondewo.survey.client.services_interface.get_keycloak_token_provider"
_ASYNC_FACTORY: str = "ondewo.survey.client.async_services_interface.get_keycloak_token_provider"

HOST: str = "localhost"
PORT: str = "50051"
USERNAME: str = "tech-user@example.com"
PASSWORD: str = "s3cr3t"
KEYCLOAK_URL: str = "https://kc.example.com/auth"
REALM: str = "ondewo-ccai-platform"
CLIENT_ID: str = "ondewo-survey-cai-sdk-public"


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
    with (
        patch(_SYNC_FACTORY, return_value=MagicMock(name="KeycloakTokenProvider")),
        patch(_ASYNC_FACTORY, return_value=MagicMock(name="KeycloakTokenProvider")),
    ):
        client: Client = Client(config=_make_config(), use_secure_channel=False)

    assert isinstance(client.services.survey, Survey)
    assert isinstance(client.services.fhir, FHIR)


def test_async_client_wires_survey_and_fhir_services() -> None:
    """The real `AsyncClient` populates `services.survey`/`services.fhir` with the right types."""
    with (
        patch(_SYNC_FACTORY, return_value=MagicMock(name="KeycloakTokenProvider")),
        patch(_ASYNC_FACTORY, return_value=MagicMock(name="KeycloakTokenProvider")),
    ):
        client: AsyncClient = AsyncClient(config=_make_config(), use_secure_channel=False)

    assert isinstance(client.services.survey, AsyncSurvey)
    assert isinstance(client.services.fhir, AsyncFHIR)


def test_async_service_wrappers_extend_the_async_services_interface() -> None:
    """The async wrappers subclass `AsyncServicesInterface`, never the synchronous one.

    `make create_async_services` copies every `services/<name>.py` to
    `services/async_<name>.py` and rewrites the copy. Its substitutions used to be keyed on
    ondewo-client-utils' `BaseServicesInterface`, so once this repo grew its own
    `ServicesInterface` (the Keycloak bearer seam) the rewrite matched nothing and the copy
    survived verbatim: `AsyncSurvey`/`AsyncFHIR` became synchronous classes behind async
    names. That happened twice and is what shipped in 2.0.2.
    """
    for wrapper in (AsyncSurvey, AsyncFHIR):
        assert issubclass(wrapper, AsyncServicesInterface)
        assert not issubclass(wrapper, ServicesInterface)


def test_async_client_opens_async_channels_and_the_sync_client_does_not() -> None:
    """`AsyncClient` builds `grpc.aio` channels; `Client` builds synchronous ones.

    This is the property the whole async surface rests on. `AsyncBaseClient.disconnect`
    awaits `grpc_channel.close(grace=None)`, which a synchronous `grpc.Channel` rejects with
    `TypeError: Channel.close() got an unexpected keyword argument 'grace'`, and the stubs
    built on a synchronous channel return responses instead of awaitables.
    """
    with (
        patch(_SYNC_FACTORY, return_value=MagicMock(name="KeycloakTokenProvider")),
        patch(_ASYNC_FACTORY, return_value=MagicMock(name="KeycloakTokenProvider")),
    ):
        async_client: AsyncClient = AsyncClient(config=_make_config(), use_secure_channel=False)
        client: Client = Client(config=_make_config(), use_secure_channel=False)

    assert isinstance(async_client.services.survey.grpc_channel, grpc.aio.Channel)
    assert isinstance(async_client.services.fhir.grpc_channel, grpc.aio.Channel)
    assert not isinstance(client.services.survey.grpc_channel, grpc.aio.Channel)
    assert not isinstance(client.services.fhir.grpc_channel, grpc.aio.Channel)
