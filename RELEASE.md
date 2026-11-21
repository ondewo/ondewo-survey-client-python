# Release History

*****************

## Release ONDEWO Survey Python Client 2.1.2

### Bug Fixes

* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) `loguru` is a runtime dependency. 2.1.1's `utils/keycloak.py` logs through it, but it was declared only in the `dev` extra, so importing the client from a wheel installed on its own raised `ModuleNotFoundError: No module named 'loguru'`; every environment that also installed `dev` hid it.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) `test_runtime_imports_are_declared.py` (shared verbatim by every python SDK) fails for any third-party module the package imports that is not a declared runtime dependency.

*****************

## Release ONDEWO Survey Python Client 2.1.1

### New Features

* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) Offline-token start-up, as ondewo-nlu-client has it: `ClientConfig.refresh_token` (appended as the last field) hands the client a Keycloak *offline* refresh token instead of a password, and the client then never sends a password grant. `KeycloakTokenProvider(refresh_token=...)` (appended as the last parameter) starts with a `grant_type=refresh_token` exchange and auto-refreshes exactly as on the password path. Keycloak's brute-force detection counts failed LOGINS, so N processes booting at once with one technical user are a burst the realm penalises, while N refresh grants of one offline token are not (measured: 3/10 password grants accepted at 0 ms spacing, 10/10 refresh grants).
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) A Keycloak config needs `password` OR `refresh_token`; when both are set the token wins, and a refused token is never answered with a password login. The token is redacted from the config's repr like the password, takes part (hashed) in the shared-provider registry key, so two token-only configs of different tenants never share a provider, and the `token_expiration_in_s` window is armed on both paths.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) Tests: `test_client_config_refresh_token.py` and the offline-token classes of `test_keycloak_refresh_resilience.py`, both shared verbatim by every python SDK.

### Bug Fixes

* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) Keycloak token refresh: a failed refresh no longer ends the background refresh thread. Any exception from the token endpoint (a 502 from a proxy, a DNS failure, a restarting Keycloak, a dead offline session) escaped the thread target and killed it, and nothing re-armed it, so the access token lapsed for the life of the process. The thread now survives every failure and retries with backoff.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) Keycloak token refresh: the per-call (lazy) refresh in `KeycloakTokenProvider.authorization_metadata()` honours the same failure backoff as the background thread, so a Keycloak outage no longer turns every gRPC call into a token request sent while the provider lock is held.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) A token that is still valid keeps being served when its refresh fails inside the 30 s expiry leeway; only an EXPIRED token raises. It raises `KeycloakAuthenticationError` whatever failed underneath: network errors (`requests.ConnectionError`, `Timeout`, `OSError`), a non-2xx status, a body that is not JSON or not a JSON object, a missing `access_token` and a non-numeric `expires_in` are all mapped to it with the original exception chained. A malformed response no longer changes any provider state.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) `KeycloakTokenProvider.stop()` (and so `__del__`) skips the thread join once the interpreter is finalizing, so process exit on CPython >= 3.13 no longer prints "Exception ignored while calling deallocator". A token response without an `access_token` is reported by its field names only, never its values (a token response is credential material).
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) `get_keycloak_token_provider` keys its shared-provider registry by a hash of the credentials instead of `id(config)`. CPython reuses a freed `ClientConfig`'s address, so a new client could be handed the PREVIOUS user's live provider and authenticate as that user.

### Improvements

* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) One Keycloak refresh implementation, byte-identical across the ondewo python SDKs (nlu, csi, s2t, sip, survey, t2s, vtsi): failed refreshes back off with full jitter from 5 s doubling up to 300 s, the background thread and the per-call path share that backoff, and a success resets it. Each failure logs one WARNING with the attempt number, the retry delay and how long the current token stays valid; the first success afterwards logs one INFO. No credential appears in either line.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) The token-endpoint HTTP timeout is 10 s (was 30 s): a refresh runs under the provider lock that every call reads its bearer token through, so this bounds how long a hung Keycloak can stall the client. Quoted Keycloak error bodies are cut at 500 characters.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) `KeycloakTokenProvider` accepts `random_fn` (the jitter source, appended as the last parameter); the backoff is measured from the moment a failure is recorded, so an attempt that hung for the whole timeout does not schedule a retry that is already due.
* [[OND236-120]](https://ondewo.atlassian.net/browse/OND236-120) New `test_keycloak_refresh_resilience.py`, shared verbatim by every python SDK: every failure kind, the backoff ladder and its bounds, the shared lazy and background backoff, the still-valid-token path, 16 threads during an outage (one token request), a real daemon thread recovering after three different failures, malformed responses, credential-free logs, `stop()` during interpreter finalization and the credential-keyed provider registry.

*****************

## Release ONDEWO Survey Python Client 2.1.0

### Improvements

* Tracking API Version [2.1.0](https://github.com/ondewo/ondewo-survey-api/releases/tag/2.1.0) ( [Documentation](https://ondewo.github.io/ondewo-survey-api/) )
* Generated with ondewo-proto-compiler 5.17.0 (grpcio-tools 1.85.1, mypy-protobuf 5.1.0). New runtime floors: Python >= 3.10, `protobuf>=7.35.1,<8`, `grpcio>=1.85.1`; `grpcio-tools` and `grpcio-reflection` are no longer runtime dependencies of this package

*****************

## Release ONDEWO Survey Python Client 2.0.3

### Bug Fixes

* [[OND211-2443]](https://ondewo.atlassian.net/browse/OND211-2443) **`ClientConfig` printed its credentials in clear text.** The `@dataclass`-generated `__repr__` rendered the Keycloak `password` and the gRPC certificate, so `log.debug(f"...{config}")` or a traceback carrying locals wrote them to the logs. `repr()` / `str()` now render `password`, `grpc_cert`, the mutual-TLS private key `grpc_client_key` and every field declared `repr=False` as `***REDACTED***`; an unset or empty secret still renders as `None` / `''`. **Behaviour change** for anyone who parsed the repr: read the attribute instead.
* [[OND211-2443]](https://ondewo.atlassian.net/browse/OND211-2443) Dependency: `ondewo-client-utils>=4.1.1` on Python >= 3.12 (`>=3.2.0` below).
* **`AsyncSurvey` / `AsyncFHIR` were synchronous in 2.0.2.** `make create_async_services` no longer matched this repo's own `ServicesInterface`, so the async wrappers were byte-identical copies of the sync ones: `AsyncClient` opened synchronous channels and `AsyncClient.disconnect()` raised `TypeError`. The generator and the wrappers are fixed, and a test guards both.
* Docs: the service interfaces no longer claim the wrappers attach the bearer token automatically; pass `metadata=` explicitly, as the examples do.
* Tooling: the duplicate `conventional-pre-commit` commit-msg hook declared after `giticket` is removed (it rejected every commit on a ticket branch); the client wiring test is hermetic (no network).
* Regenerated with [ondewo-proto-compiler 5.15.2](https://github.com/ondewo/ondewo-proto-compiler/releases/tag/5.15.2).

*****************

## Release ONDEWO Survey Python Client 2.0.2

### Bug Fixes

* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Regenerated with [ondewo-proto-compiler 5.13.0](https://github.com/ondewo/ondewo-proto-compiler/releases/tag/5.13.0).
* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Tooling: `conventional-pre-commit` now runs before `giticket` at the commit-msg stage - with giticket first, its `[OND221-2830] fix: ...` rewrite was no longer valid Conventional Commits and every commit on a ticket branch failed. `README.md` is prettier-ignored where `.prettierrc` sets `useTabs` and markdownlint's MD010 de-tabs the same blocks, and the codegen `docker run` invocations no longer pass `-it`, which fails outside a TTY.

*****************

## Release ONDEWO Survey Python Client 2.0.1

### Improvements

* Added functionality to pass grpc options to grpc clients based on [ONDEWO CLIENT UTILS PYTHON 2.0.0](https://github.com/ondewo/ondewo-client-utils-python/releases/tag/2.0.0)

*****************

## Release ONDEWO Survey Python Client 2.0.0

### Improvements

* Tracking API Version [2.0.0](https://github.com/ondewo/ondewo-survey-api/releases/tag/2.0.0) ( [Documentation](https://ondewo.github.io/ondewo-survey-api/) )

*****************

## Release ONDEWO Survey Python Client 1.1.0

### Improvements

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Added pre-commit hooks and adjusted files to them
* Updated API to 1.1.0

*****************

## Release ONDEWO Survey Python Client 1.0.1

### Bug fixes

* Relaxed requirements to ondewo-client-utils>=0.1.0

*****************

## Release ONDEWO Survey Python Client 1.0.0

### New Features

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Automated Release Process

*****************

## Release ONDEWO Survey Python Client 0.6.0

### New Features

* Extension of the API to support the FHIR format

*****************

## Release ONDEWO Survey Python Client 0.5.1

### Bug Fixes

* Addition of a missing init file that prevented the installation through PyPi

*****************

## Release ONDEWO Survey Python Client 0.5.0

### New Features

* Adapted to support the Survey API 0.5.0

*****************

## Release ONDEWO Survey Python Client 0.4.0

### Bug Fixes

* Correct release version from 0.1.0 to 0.4.0

### New Features

* [[OND212-33]](https://ondewo.atlassian.net/browse/OND212-33) - Initialise repository for the Survey Server Python client

*****************

## Release ONDEWO Survey Python Client 0.1.0

### New Features

* [[OND212-33]](https://ondewo.atlassian.net/browse/OND212-33) - Initialise repository for the Survey Server Python client

*****************
