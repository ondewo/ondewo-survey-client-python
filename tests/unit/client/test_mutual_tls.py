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
"""End-to-end TLS and mutual TLS through the real SURVEY ``Client`` / ``AsyncClient``.

Every handshake test builds the SDK's own ``ClientConfig`` and ``Client`` (or ``AsyncClient``)
against a real in-process gRPC server on an ephemeral port, with certificates minted per test
module (nothing private is committed). The server has no servicer, so an RPC that completes the
handshake is answered ``UNIMPLEMENTED``; that answer proves the TLS (and client-certificate)
handshake succeeded through both the FHIR and the Survey service channels. A refused handshake
surfaces as ``UNAVAILABLE``, never as a crash.

The RPCs used (``CreateSurvey`` / ``CreateFHIRSurvey``) are not idempotent, so the SDK's retry
policy does not retry them and a refused handshake fails at once instead of at the deadline.
"""

import datetime
from concurrent import futures
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
)

import grpc
import pytest
import pytest_asyncio
from cryptography import x509
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import (
    ExtendedKeyUsageOID,
    NameOID,
)

from ondewo.survey.client.async_client import AsyncClient
from ondewo.survey.client.client import Client
from ondewo.survey.client.client_config import ClientConfig
from ondewo.survey.fhir_pb2 import CreateFHIRSurveyRequest
from ondewo.survey.survey_pb2 import CreateSurveyRequest

SERVER_NAME: str = "localhost"
TIMEOUT_IN_S: float = 10.0
USER_NAME: str = "tech-user@example.com"
PASSWORD: str = "s3cr3t-password"


class Pki:
    """One throwaway CA with a server leaf (SAN ``localhost``) and a client leaf, all PEM bytes."""

    def __init__(self, name: str) -> None:
        self._ca_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        self.ca_cert: bytes = self._issue(f"{name}-ca", self._ca_key.public_key(), ca=True, issuer=None)
        ca: x509.Certificate = x509.load_pem_x509_certificate(self.ca_cert)
        server_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        self.server_key: bytes = _pem_key(server_key)
        self.server_cert: bytes = self._issue(
            f"{name}-server",
            server_key.public_key(),
            ca=False,
            issuer=ca,
            usage=ExtendedKeyUsageOID.SERVER_AUTH,
            san=SERVER_NAME,
        )
        client_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        self.client_key: bytes = _pem_key(client_key)
        self.client_cert: bytes = self._issue(
            f"{name}-client",
            client_key.public_key(),
            ca=False,
            issuer=ca,
            usage=ExtendedKeyUsageOID.CLIENT_AUTH,
        )

    def _issue(
        self,
        subject: str,
        public_key: ec.EllipticCurvePublicKey,
        ca: bool,
        issuer: Optional[x509.Certificate],
        usage: Optional[x509.ObjectIdentifier] = None,
        san: Optional[str] = None,
    ) -> bytes:
        now: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        name: x509.Name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject)])
        builder: x509.CertificateBuilder = (
            x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name if issuer is None else issuer.subject)
            .public_key(public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=30))
            .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True)
        )
        if usage is not None:
            builder = builder.add_extension(x509.ExtendedKeyUsage([usage]), critical=False)
        if san is not None:
            builder = builder.add_extension(x509.SubjectAlternativeName([x509.DNSName(san)]), critical=False)
        return builder.sign(self._ca_key, hashes.SHA256()).public_bytes(serialization.Encoding.PEM)


def _pem_key(key: ec.EllipticCurvePrivateKey) -> bytes:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


@pytest.fixture(scope="module")
def pki() -> Pki:
    return Pki("deployment")


@pytest.fixture(scope="module")
def foreign() -> Pki:
    return Pki("foreign")


def _server_credentials(pki: Pki, require_client_auth: bool) -> grpc.ServerCredentials:
    return grpc.ssl_server_credentials(
        [(pki.server_key, pki.server_cert)],
        root_certificates=pki.ca_cert if require_client_auth else None,
        require_client_auth=require_client_auth,
    )


def _config(port: int, trust: Pki, client: Optional[Pki] = None, crlf: bool = False) -> ClientConfig:
    """A survey config trusting ``trust``'s CA, presenting ``client``'s leaf when given (mutual TLS)."""

    def pem(value: bytes) -> str:
        return (value.replace(b"\n", b"\r\n") if crlf else value).decode()

    return ClientConfig(
        host=SERVER_NAME,
        port=str(port),
        user_name=USER_NAME,
        password=PASSWORD,
        grpc_cert=pem(trust.ca_cert),
        grpc_client_cert=None if client is None else pem(client.client_cert),
        grpc_client_key=None if client is None else pem(client.client_key),
    )


@pytest.fixture
def server() -> Iterator[Callable[[Pki, bool], int]]:
    """Start a servicer-less TLS server on an ephemeral port; ``(pki, require_client_auth) -> port``."""
    servers: List[grpc.Server] = []

    def start(pki: Pki, require_client_auth: bool) -> int:
        grpc_server: grpc.Server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        port: int = grpc_server.add_secure_port(f"{SERVER_NAME}:0", _server_credentials(pki, require_client_auth))
        grpc_server.start()
        servers.append(grpc_server)
        return port

    yield start
    for grpc_server in servers:
        grpc_server.stop(grace=None)


def _call_both_services(config: ClientConfig) -> None:
    """Call one RPC on each of the client's services; both must reach the server (``UNIMPLEMENTED``)."""
    client: Client = Client(config=config, use_secure_channel=True)
    try:
        for call in (
            lambda: client.services.survey.stub.CreateSurvey(CreateSurveyRequest(), timeout=TIMEOUT_IN_S),
            lambda: client.services.fhir.stub.CreateFHIRSurvey(CreateFHIRSurveyRequest(), timeout=TIMEOUT_IN_S),
        ):
            with pytest.raises(grpc.RpcError) as answer:
                call()
            assert answer.value.code() is grpc.StatusCode.UNIMPLEMENTED  # type: ignore[attr-defined]
    finally:
        client.disconnect()


def _refused_code(config: ClientConfig) -> grpc.StatusCode:
    client: Client = Client(config=config, use_secure_channel=True)
    try:
        with pytest.raises(grpc.RpcError) as refusal:
            client.services.survey.stub.CreateSurvey(CreateSurveyRequest(), timeout=TIMEOUT_IN_S)
        code: grpc.StatusCode = refusal.value.code()  # type: ignore[attr-defined]
        return code
    finally:
        client.disconnect()


class TestSyncClientHandshakes:
    def test_plain_tls(self, server: Callable[[Pki, bool], int], pki: Pki) -> None:
        _call_both_services(_config(server(pki, False), pki))

    def test_mutual_tls(self, server: Callable[[Pki, bool], int], pki: Pki) -> None:
        _call_both_services(_config(server(pki, True), pki, client=pki))

    def test_mutual_tls_with_crlf_pems(self, server: Callable[[Pki, bool], int], pki: Pki) -> None:
        _call_both_services(_config(server(pki, True), pki, client=pki, crlf=True))

    def test_tls_only_server_accepts_a_client_presenting_a_leaf(
        self, server: Callable[[Pki, bool], int], pki: Pki
    ) -> None:
        _call_both_services(_config(server(pki, False), pki, client=pki))

    def test_no_identity_against_a_client_auth_server_is_unavailable(
        self, server: Callable[[Pki, bool], int], pki: Pki
    ) -> None:
        assert _refused_code(_config(server(pki, True), pki)) is grpc.StatusCode.UNAVAILABLE

    def test_identity_from_an_unrelated_ca_is_refused(
        self, server: Callable[[Pki, bool], int], pki: Pki, foreign: Pki
    ) -> None:
        assert _refused_code(_config(server(pki, True), pki, client=foreign)) is grpc.StatusCode.UNAVAILABLE

    def test_the_client_still_verifies_the_server(
        self, server: Callable[[Pki, bool], int], pki: Pki, foreign: Pki
    ) -> None:
        assert _refused_code(_config(server(pki, False), foreign)) is grpc.StatusCode.UNAVAILABLE


class TestAsyncClientHandshakes:
    @pytest_asyncio.fixture
    async def aio_server(self) -> Any:
        """Start a servicer-less ``grpc.aio`` TLS server; ``(pki, require_client_auth) -> port``."""
        servers: List[grpc.aio.Server] = []

        async def start(pki: Pki, require_client_auth: bool) -> int:
            grpc_server: grpc.aio.Server = grpc.aio.server()
            port: int = grpc_server.add_secure_port(f"{SERVER_NAME}:0", _server_credentials(pki, require_client_auth))
            await grpc_server.start()
            servers.append(grpc_server)
            return port

        yield start
        for grpc_server in servers:
            await grpc_server.stop(grace=None)

    @staticmethod
    async def _code(config: ClientConfig) -> grpc.StatusCode:
        client: AsyncClient = AsyncClient(config=config, use_secure_channel=True)
        try:
            with pytest.raises(grpc.aio.AioRpcError) as answer:
                await client.services.fhir.stub.CreateFHIRSurvey(CreateFHIRSurveyRequest(), timeout=TIMEOUT_IN_S)
            with pytest.raises(grpc.aio.AioRpcError) as survey_answer:
                await client.services.survey.stub.CreateSurvey(CreateSurveyRequest(), timeout=TIMEOUT_IN_S)
            assert survey_answer.value.code() is answer.value.code()
            return answer.value.code()
        finally:
            await client.disconnect()

    @pytest.mark.asyncio
    async def test_plain_tls(self, aio_server: Any, pki: Pki) -> None:
        assert await self._code(_config(await aio_server(pki, False), pki)) is grpc.StatusCode.UNIMPLEMENTED

    @pytest.mark.asyncio
    async def test_mutual_tls(self, aio_server: Any, pki: Pki) -> None:
        config: ClientConfig = _config(await aio_server(pki, True), pki, client=pki)
        assert await self._code(config) is grpc.StatusCode.UNIMPLEMENTED

    @pytest.mark.asyncio
    async def test_no_identity_against_a_client_auth_server_is_unavailable(self, aio_server: Any, pki: Pki) -> None:
        assert await self._code(_config(await aio_server(pki, True), pki)) is grpc.StatusCode.UNAVAILABLE

    @pytest.mark.asyncio
    async def test_identity_from_an_unrelated_ca_is_refused(self, aio_server: Any, pki: Pki, foreign: Pki) -> None:
        config: ClientConfig = _config(await aio_server(pki, True), pki, client=foreign)
        assert await self._code(config) is grpc.StatusCode.UNAVAILABLE


class TestConfigEdgeCases:
    @pytest.mark.parametrize("half", ["grpc_client_cert", "grpc_client_key"])
    def test_half_a_client_identity_is_refused_by_the_config(self, pki: Pki, half: str) -> None:
        """Half a pair would make grpc core abort() the process; the config refuses it before any channel."""
        value: Dict[str, Any] = {half: (pki.client_cert if half == "grpc_client_cert" else pki.client_key).decode()}
        with pytest.raises(ValueError, match="set both to use mutual TLS, or neither") as refusal:
            ClientConfig(
                host=SERVER_NAME,
                port="1",
                user_name=USER_NAME,
                password=PASSWORD,
                grpc_cert=pki.ca_cert.decode(),
                **value,
            )
        assert "PRIVATE KEY" not in str(refusal.value)
        assert "CERTIFICATE" not in str(refusal.value)

    def test_empty_identity_on_both_is_plain_tls(self, server: Callable[[Pki, bool], int], pki: Pki) -> None:
        port: int = server(pki, False)
        config: ClientConfig = ClientConfig(
            host=SERVER_NAME,
            port=str(port),
            user_name=USER_NAME,
            password=PASSWORD,
            grpc_cert=pki.ca_cert.decode(),
            grpc_client_cert="",
            grpc_client_key="",
        )
        _call_both_services(config)

    @pytest.mark.parametrize("client_class", [Client, AsyncClient])
    def test_insecure_channel_with_a_client_identity_is_refused(self, pki: Pki, client_class: Any) -> None:
        config: ClientConfig = _config(1, pki, client=pki)
        with pytest.raises(ValueError, match="use a secure channel") as refusal:
            client_class(config=config, use_secure_channel=False)
        assert "PRIVATE KEY" not in str(refusal.value)
        assert PASSWORD not in str(refusal.value)

    def test_repr_and_str_never_render_the_key_or_password(self, pki: Pki) -> None:
        config: ClientConfig = _config(1, pki, client=pki)
        key_body: str = pki.client_key.decode().splitlines()[1]
        for rendered in (repr(config), str(config)):
            assert key_body not in rendered
            assert "PRIVATE KEY" not in rendered
            assert PASSWORD not in rendered
            assert "grpc_client_key='***REDACTED***'" in rendered
            assert "password='***REDACTED***'" in rendered
