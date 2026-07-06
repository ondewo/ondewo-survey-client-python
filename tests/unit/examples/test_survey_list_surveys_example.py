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
"""Hermetic unit tests for the `survey_list_surveys_example` example.

No live server and no Keycloak network call are involved: the gRPC stub and the shared
Keycloak token provider are both replaced with fakes, so the tests prove the example
builds the right request, attaches the bearer metadata, and handles the response.
"""
import importlib.util
import os
from types import (
    ModuleType,
    SimpleNamespace,
)
from typing import (
    List,
    Tuple,
)
from unittest.mock import MagicMock

import pytest

from ondewo.survey.client.client_config import ClientConfig
from ondewo.survey.survey_pb2 import (
    ListSurveysRequest,
    ListSurveysResponse,
    Survey,
)

# Bound exactly once so a refactor that changes only an input or only an expectation cannot
# silently make a test tautological.
ACCESS_TOKEN: str = 'test-access-token'
BEARER_METADATA: List[Tuple[str, str]] = [('authorization', f'Bearer {ACCESS_TOKEN}')]
EXPECTED_PAGE_TOKEN: str = 'page_size-10000'

HOST: str = 'survey.example.com'
PORT: str = '50051'
USERNAME: str = 'tech-user@ondewo.com'
PASSWORD: str = 's3cr3t'
KEYCLOAK_URL: str = 'https://kc.example.com/auth'
REALM: str = 'ondewo-ccai-platform'
CLIENT_ID: str = 'ondewo-survey-cai-sdk-public'

_REPO_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
_EXAMPLE_PATH: str = os.path.join(_REPO_ROOT, 'examples', 'survey_list_surveys_example.py')


def _load_example() -> ModuleType:
    """Load the standalone example module by file path (it is not an importable package).

    Returns:
        ModuleType:
            The freshly imported `survey_list_surveys_example` module.
    """
    spec = importlib.util.spec_from_file_location('survey_list_surveys_example', _EXAMPLE_PATH)
    assert spec is not None and spec.loader is not None
    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _make_config() -> ClientConfig:
    """Build a Keycloak-path `ClientConfig` used across the tests.

    Returns:
        ClientConfig:
            A valid config flagged for the D18 Keycloak auth path.
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


def _fake_provider() -> MagicMock:
    """Build a stand-in Keycloak token provider that yields the canned bearer metadata.

    Returns:
        MagicMock:
            A provider whose `bearer_metadata()` returns `BEARER_METADATA`.
    """
    provider: MagicMock = MagicMock(name='KeycloakTokenProvider')
    provider.bearer_metadata.return_value = BEARER_METADATA
    return provider


def _fake_client_returning(response: ListSurveysResponse) -> SimpleNamespace:
    """Build a fake client whose `survey` stub returns `response` from `ListSurveys`.

    Args:
        response (ListSurveysResponse):
            The response the mocked `ListSurveys` RPC should return.

    Returns:
        SimpleNamespace:
            A client shaped like `client.services.survey.stub.ListSurveys`, with a
            `MagicMock` stub and a `disconnect` mock.
    """
    stub: MagicMock = MagicMock(name='SurveysStub')
    stub.ListSurveys.return_value = response
    client: SimpleNamespace = SimpleNamespace(
        services=SimpleNamespace(survey=SimpleNamespace(stub=stub)),
        disconnect=MagicMock(name='disconnect'),
    )
    return client


class TestBuildClientConfig:
    """`build_client_config()` reads the environment into a Keycloak-path config."""

    def test_reads_env_into_keycloak_config(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The env vars populate the config and flag the Keycloak auth path.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to set the connection/credential env vars.
        """
        monkeypatch.setenv('ONDEWO_HOST', HOST)
        monkeypatch.setenv('ONDEWO_PORT', PORT)
        monkeypatch.setenv('KEYCLOAK_USER_NAME', USERNAME)
        monkeypatch.setenv('KEYCLOAK_PASSWORD', PASSWORD)
        monkeypatch.setenv('KEYCLOAK_URL', KEYCLOAK_URL)
        monkeypatch.setenv('KEYCLOAK_REALM', REALM)
        monkeypatch.setenv('KEYCLOAK_CLIENT_ID', CLIENT_ID)

        example: ModuleType = _load_example()
        config: ClientConfig = example.build_client_config()

        assert config.host == HOST
        assert config.port == PORT
        assert config.user_name == USERNAME
        assert config.client_id == CLIENT_ID
        assert config.use_keycloak is True


class TestListSurveys:
    """`list_surveys()` builds the request, attaches bearer metadata, and returns surveys."""

    def test_builds_request_attaches_metadata_and_returns_surveys(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """The RPC is called with a `page_size-10000` request and the bearer metadata.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the shared Keycloak provider factory with a fake.
        """
        example: ModuleType = _load_example()

        surveys: List[Survey] = [
            Survey(survey_id='sid-1', display_name='Customer NPS', language_code='en'),
            Survey(survey_id='sid-2', display_name='Onboarding', language_code='de'),
        ]
        response: ListSurveysResponse = ListSurveysResponse(surveys=surveys, next_page_token='')
        client: SimpleNamespace = _fake_client_returning(response)

        provider: MagicMock = _fake_provider()
        captured_config: List[ClientConfig] = []

        def fake_get_provider(config: ClientConfig) -> MagicMock:
            captured_config.append(config)
            return provider

        monkeypatch.setattr(example, 'get_keycloak_token_provider', fake_get_provider)

        config: ClientConfig = _make_config()
        result: List[Survey] = example.list_surveys(client=client, config=config)

        # The response surveys are returned verbatim as a list.
        assert result == surveys

        # The shared provider was looked up for exactly this config.
        assert captured_config == [config]

        # The stub was called once with the paginated request and the bearer metadata.
        stub: MagicMock = client.services.survey.stub
        stub.ListSurveys.assert_called_once()
        call_kwargs = stub.ListSurveys.call_args.kwargs
        assert call_kwargs['request'] == ListSurveysRequest(page_token=EXPECTED_PAGE_TOKEN)
        assert call_kwargs['metadata'] == BEARER_METADATA


class TestMain:
    """`main()` wires the client, prints a summary, and always disconnects."""

    def test_prints_summary_and_disconnects(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """`main()` prints one line per survey and disconnects the client afterwards.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace `Client` and the Keycloak provider factory.
            capsys (pytest.CaptureFixture[str]):
                Fixture capturing stdout to assert on the printed summary.
        """
        example: ModuleType = _load_example()

        surveys: List[Survey] = [
            Survey(survey_id='sid-1', display_name='Customer NPS', language_code='en'),
        ]
        response: ListSurveysResponse = ListSurveysResponse(surveys=surveys, next_page_token='')
        client: SimpleNamespace = _fake_client_returning(response)

        # Replace the real Client constructor so no gRPC channel is opened.
        monkeypatch.setattr(example, 'Client', MagicMock(return_value=client))
        monkeypatch.setattr(example, 'get_keycloak_token_provider', lambda config: _fake_provider())

        example.main()

        captured = capsys.readouterr()
        assert 'Retrieved 1 survey(s):' in captured.out
        assert 'sid-1: Customer NPS [en]' in captured.out

        # main() must disconnect the client in its finally block.
        client.disconnect.assert_called_once_with()
