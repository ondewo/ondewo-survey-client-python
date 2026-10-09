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

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Dict,
    Type,
)

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
PLANTED_PASSWORD: str = "PLANTED-password-6b21fa"
GRPC_CERT: str = "PLANTED-BEGIN-CERTIFICATE-91cd3e"
HIDDEN: str = "PLANTED-repr-false-value-58d2a1"


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


def _config(config_class: Type[ClientConfig] = ClientConfig, **overrides: Any) -> ClientConfig:
    """Build a config carrying every secret, each a distinctive planted value.

    Args:
        config_class (Type[ClientConfig]):
            The class to instantiate (a subclass in the `repr=False` test).
        **overrides (Any):
            Field values replacing the defaults below.

    Returns:
        ClientConfig:
            The config.
    """
    kwargs: Dict[str, Any] = {
        "host": HOST,
        "port": PORT,
        "user_name": USERNAME,
        "password": PLANTED_PASSWORD,
        "grpc_cert": GRPC_CERT,
        # __post_init__ refuses half a client identity, so set both cert and key.
        "grpc_client_cert": CLIENT_CERT,
        "grpc_client_key": CLIENT_KEY,
    }
    kwargs.update(overrides)
    return config_class(**kwargs)


class TestClientConfigReprRedactsSecrets:
    """`repr()` / `str()` must not print the password, the certificate or the mutual-TLS private key.

    The assertions are behavioural (build the object, read its `repr`) rather than a source grep,
    because a grep for `__repr__` passes just as well for a `__repr__` that prints the secret anyway.
    """

    def test_the_password_is_not_printed(self) -> None:
        """The ROPC password appears in neither `repr()` nor `str()`; the marker does.

        Returns:
            None
        """
        config: ClientConfig = _config()

        # Read the ATTRIBUTE to prove the secret is really on the object; repr is the thing under test.
        assert config.password == PLANTED_PASSWORD
        assert PLANTED_PASSWORD not in repr(config)
        assert PLANTED_PASSWORD not in str(config)
        assert "password='***REDACTED***'" in repr(config)

    def test_the_grpc_certificate_is_not_printed(self) -> None:
        """The server certificate is redacted.

        Returns:
            None
        """
        config: ClientConfig = _config()

        # BaseClientConfig.__post_init__ encodes the certificate, so the stored value is bytes.
        assert config.grpc_cert == GRPC_CERT.encode()
        assert GRPC_CERT not in repr(config)
        assert "grpc_cert='***REDACTED***'" in repr(config)

    def test_the_mutual_tls_private_key_is_not_printed(self) -> None:
        """The client private key appears in neither `repr()` nor `str()`; the marker does.

        Returns:
            None
        """
        config: ClientConfig = _config()

        assert config.grpc_client_key == CLIENT_KEY.encode()
        assert CLIENT_KEY not in repr(config)
        assert CLIENT_KEY not in str(config)
        assert "grpc_client_key='***REDACTED***'" in repr(config)

    def test_an_unset_secret_is_not_reported_as_present(self) -> None:
        """An empty secret renders as `''`, not as the marker, which would read as "set".

        Returns:
            None
        """
        rendered: str = repr(_config(grpc_cert="", grpc_client_cert="", grpc_client_key=""))

        assert "grpc_cert=''" in rendered
        assert "grpc_client_key=''" in rendered

    def test_any_field_declared_repr_false_is_redacted(self) -> None:
        """A field declared `repr=False` is redacted without being named in `SECRET_FIELD_NAMES`.

        Returns:
            None
        """

        @dataclass(frozen=True, repr=False)
        class _ConfigWithHiddenField(ClientConfig):
            planted_hidden: str = field(default="", repr=False)

        config: ClientConfig = _config(config_class=_ConfigWithHiddenField, planted_hidden=HIDDEN)

        assert getattr(config, "planted_hidden") == HIDDEN
        assert HIDDEN not in repr(config)
        assert "planted_hidden='***REDACTED***'" in repr(config)

    def test_the_non_secret_fields_survive(self) -> None:
        """Redaction must not be satisfied by printing nothing: host and user stay visible.

        Returns:
            None
        """
        rendered: str = repr(_config())

        assert HOST in rendered
        assert USERNAME in rendered
