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
"""Unit tests for `ClientConfig` validation on the bearer-only auth model (D18)."""

import pytest

from ondewo.survey.client.client_config import ClientConfig

HOST: str = "localhost"
PORT: str = "50055"
USERNAME: str = "tech-user@example.com"
PASSWORD: str = "s3cr3t"
KEYCLOAK_URL: str = "https://kc.example.com/auth"
REALM: str = "ondewo-ccai-platform"
CLIENT_ID: str = "ondewo-survey-cai-sdk-public"
#: Distinctive, so a match in a repr cannot be a coincidence of a field name or a host.
CLIENT_CERT: str = "PLANTED-BEGIN-CLIENT-CERTIFICATE-3a7c52"
CLIENT_KEY: str = "PLANTED-BEGIN-PRIVATE-KEY-e04b9d"


class TestNonKeycloakPath:
    """Validation of a config with no Keycloak fields (calls travel unauthenticated)."""

    def test_config_without_keycloak_is_valid_and_not_keycloak(self) -> None:
        """A config with only user_name/password is valid and reports `use_keycloak is False`.

        Returns:
            None
        """
        config = ClientConfig(host=HOST, port=PORT, user_name=USERNAME, password=PASSWORD)

        assert config.use_keycloak is False

    def test_no_http_token_field_present(self) -> None:
        """The bearer-only config exposes no legacy `http_token` attribute.

        Returns:
            None
        """
        config = ClientConfig(host=HOST, port=PORT, user_name=USERNAME, password=PASSWORD)

        assert not hasattr(config, "http_token")

    def test_missing_user_name_raises(self) -> None:
        """Omitting `user_name` raises `ValueError` (mandatory for the bearer-only path).

        Returns:
            None
        """
        with pytest.raises(ValueError):
            ClientConfig(host=HOST, port=PORT, password=PASSWORD)

    def test_missing_password_raises(self) -> None:
        """Omitting `password` raises `ValueError` (mandatory for the bearer-only path).

        Returns:
            None
        """
        with pytest.raises(ValueError):
            ClientConfig(host=HOST, port=PORT, user_name=USERNAME)


class TestKeycloakPath:
    """Validation of the Keycloak headless offline-token auth path (D18)."""

    def test_full_keycloak_config_is_valid_and_flagged(self) -> None:
        """A complete Keycloak config is accepted and flagged via `use_keycloak`.

        Returns:
            None
        """
        config = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            token_expiration_in_s=3600,
        )

        assert config.use_keycloak is True
        assert config.token_expiration_in_s == 3600
        assert config.client_id == CLIENT_ID

    def test_token_expiration_optional_defaults_none(self) -> None:
        """`token_expiration_in_s` defaults to `None` while still enabling the Keycloak path.

        Returns:
            None
        """
        config = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
        )

        assert config.token_expiration_in_s is None
        assert config.use_keycloak is True

    def test_partial_keycloak_config_raises(self) -> None:
        """A partially filled Keycloak triple raises `ValueError` (all-or-nothing).

        Returns:
            None
        """
        # realm + client_id missing while keycloak_url is set → all-or-nothing violation.
        with pytest.raises(ValueError):
            ClientConfig(
                host=HOST,
                port=PORT,
                user_name=USERNAME,
                password=PASSWORD,
                keycloak_url=KEYCLOAK_URL,
            )

    def test_no_client_secret_field_present(self) -> None:
        """The config exposes no `client_secret` attribute (public SDK client, Q1).

        Returns:
            None
        """
        # Q1: the public SDK client has no client_secret — the config must not expose one.
        config = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
        )

        assert not hasattr(config, "client_secret")


class TestMutualTlsKeyIsNotPrinted:
    """`repr()` / `str()` of a config with a mutual-TLS client identity must not print the private key."""

    def test_the_mutual_tls_private_key_is_not_printed(self) -> None:
        """The client private key appears in neither `repr()` nor `str()`.

        `BaseClientConfig` declares `grpc_client_key` with `repr=False`. This class keeps the
        `__repr__` that `@dataclass` generates, which honours that flag; the test pins it so a
        hand-written `__repr__` (as the nlu/s2t/t2s twins have) cannot reintroduce the leak.

        Returns:
            None
        """
        # __post_init__ refuses half a client identity, so set both cert and key.
        config = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            password=PASSWORD,
            grpc_client_cert=CLIENT_CERT,
            grpc_client_key=CLIENT_KEY,
        )

        # Read the ATTRIBUTE to prove the key is really on the object (encoded to bytes).
        assert config.grpc_client_key == CLIENT_KEY.encode()
        assert CLIENT_KEY not in repr(config)
        assert CLIENT_KEY not in str(config)
