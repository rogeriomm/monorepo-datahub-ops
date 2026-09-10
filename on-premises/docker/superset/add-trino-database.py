#!/usr/bin/env python3

from __future__ import annotations

import http.cookiejar
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


# Run this script inside the Compose tools container. These service names and
# ports are reachable through the shared backend network.
SUPERSET_URL = "http://superset:8088"
DATABASE_NAME = "Trino"
SQLALCHEMY_URI = "trino://trino-client@trino:8443/system"

ENCRYPTED_EXTRA = {
    "auth_method": "certificate",
    "auth_params": {
        "cert": "/etc/trino/tls/trino-client.crt",
        "key": "/etc/trino/tls/trino-client-key",
    },
}
EXTRA = {
    "engine_params": {
        "connect_args": {"verify": "/etc/trino/tls/ca.crt"},
    },
}


class SupersetApiError(RuntimeError):
    pass


class SupersetClient:
    def __init__(self) -> None:
        cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookie_jar)
        )
        self.access_token: str | None = None
        self.csrf_token: str | None = None

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        payload: dict[str, Any] | None = None,
        query: dict[str, str] | None = None,
        authenticate: bool = True,
        include_csrf_token: bool = False,
    ) -> dict[str, Any]:
        url = f"{SUPERSET_URL}{endpoint}"
        if query:
            url = f"{url}?{urllib.parse.urlencode(query)}"

        headers = {"Accept": "application/json"}
        if authenticate:
            if not self.access_token:
                raise SupersetApiError("Superset access token is missing")
            headers["Authorization"] = f"Bearer {self.access_token}"

        if include_csrf_token:
            if not self.csrf_token:
                raise SupersetApiError("Superset CSRF token is missing")
            headers["X-CSRFToken"] = self.csrf_token

        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode()

        api_request = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method=method,
        )

        try:
            with self.opener.open(api_request, timeout=30) as response:
                body = response.read().decode(
                    response.headers.get_content_charset() or "utf-8"
                )
        except urllib.error.HTTPError as error:
            body = error.read().decode(
                error.headers.get_content_charset() or "utf-8",
                errors="replace",
            )
            raise SupersetApiError(
                f"{method} {endpoint} returned HTTP {error.code}: {body}"
            ) from error
        except urllib.error.URLError as error:
            raise SupersetApiError(
                f"Unable to reach Superset at {SUPERSET_URL}. "
                "Run this script inside the Compose tools container."
            ) from error

        if not body:
            return {}

        try:
            result = json.loads(body)
        except json.JSONDecodeError as error:
            raise SupersetApiError(
                f"{method} {endpoint} returned invalid JSON: {body}"
            ) from error

        if not isinstance(result, dict):
            raise SupersetApiError(
                f"{method} {endpoint} returned an unexpected JSON response"
            )
        return result

    def login(self, username: str, password: str) -> None:
        result = self.request(
            "POST",
            "/api/v1/security/login",
            payload={
                "username": username,
                "password": password,
                "provider": "db",
                "refresh": True,
            },
            authenticate=False,
        )
        access_token = result.get("access_token")
        if not isinstance(access_token, str) or not access_token:
            raise SupersetApiError(
                "Superset login succeeded without returning an access token"
            )
        self.access_token = access_token

    def load_csrf_token(self) -> None:
        result = self.request("GET", "/api/v1/security/csrf_token/")
        csrf_token = result.get("result")
        if not isinstance(csrf_token, str) or not csrf_token:
            raise SupersetApiError("Superset did not return a CSRF token")
        self.csrf_token = csrf_token


def connection_payload() -> dict[str, Any]:
    return {
        "database_name": DATABASE_NAME,
        "sqlalchemy_uri": SQLALCHEMY_URI,
        "configuration_method": "sqlalchemy_form",
        "encrypted_extra": json.dumps(ENCRYPTED_EXTRA, separators=(",", ":")),
        "extra": json.dumps(EXTRA, separators=(",", ":")),
    }


def main() -> int:
    username = os.environ.get("SUPERSET_USERNAME", "admin")
    password = os.environ.get("SUPERSET_PASSWORD", "admin")

    client = SupersetClient()
    client.login(username, password)

    databases = client.request(
        "GET",
        "/api/v1/database/",
        query={
            "q": f"(filters:!((col:database_name,opr:eq,value:{DATABASE_NAME})))",
        },
    )
    existing_count = databases.get("count")
    if not isinstance(existing_count, int):
        raise SupersetApiError(
            "Superset returned an unexpected database-list response"
        )
    if existing_count > 0:
        print(f"Superset database connection '{DATABASE_NAME}' already exists.")
        return 0

    client.load_csrf_token()
    payload = connection_payload()
    client.request(
        "POST",
        "/api/v1/database/test_connection/",
        payload=payload,
        include_csrf_token=True,
    )

    payload["expose_in_sqllab"] = True
    result = client.request(
        "POST",
        "/api/v1/database/",
        payload=payload,
        include_csrf_token=True,
    )

    database_id = result.get("id")
    if isinstance(database_id, int):
        print(
            f"Added Superset database connection '{DATABASE_NAME}' "
            f"with ID {database_id}."
        )
    else:
        print(f"Added Superset database connection '{DATABASE_NAME}'.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SupersetApiError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
