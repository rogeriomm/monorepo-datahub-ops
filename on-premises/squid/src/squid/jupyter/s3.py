from __future__ import annotations

import os
import shlex
import subprocess
from collections.abc import Mapping, Sequence

from squid.resources.s3 import S3Config, get_s3_config


class S3MagicError(RuntimeError):
    """Raised when the AWS CLI cannot run an ``%s3`` command."""


def _aws_command(arguments: Sequence[str], config: S3Config) -> list[str]:
    command = ["aws"]
    if config.endpoint_url is not None:
        command.extend(("--endpoint-url", config.endpoint_url))
    if config.region_name is not None:
        command.extend(("--region", config.region_name))
    if config.verify is False:
        command.append("--no-verify-ssl")
    elif isinstance(config.verify, str):
        command.extend(("--ca-bundle", config.verify))
    command.append("s3")
    command.extend(arguments)
    return command


def _aws_environment(config: S3Config) -> dict[str, str]:
    environment = dict(os.environ)
    environment["AWS_PAGER"] = ""
    environment["AWS_CLI_AUTO_PROMPT"] = "off"

    if config.aws_access_key_id is not None:
        environment["AWS_ACCESS_KEY_ID"] = config.aws_access_key_id
        environment["AWS_SECRET_ACCESS_KEY"] = config.aws_secret_access_key or ""
        # Static SeaweedFS credentials must not inherit a session token from
        # the notebook process.
        environment.pop("AWS_SESSION_TOKEN", None)
        environment.pop("AWS_SECURITY_TOKEN", None)
    return environment


def _stream_command(command: Sequence[str], environment: Mapping[str, str]) -> None:
    try:
        process = subprocess.Popen(
            command,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except FileNotFoundError as error:
        raise S3MagicError(
            "The AWS CLI executable 'aws' is not installed or is not on PATH"
        ) from error

    assert process.stdout is not None
    try:
        for output_line in process.stdout:
            print(output_line, end="")
    except KeyboardInterrupt:
        process.terminate()
        process.wait()
        raise

    return_code = process.wait()
    if return_code != 0:
        raise S3MagicError(f"AWS CLI exited with status {return_code}")


def run_s3(line: str) -> None:
    """Run ``aws s3`` with Squid's environment-aware S3 configuration."""
    try:
        arguments = shlex.split(line)
    except ValueError as error:
        raise S3MagicError(f"Invalid command line: {error}") from error

    if not arguments:
        arguments = ["help"]

    config = get_s3_config()
    _stream_command(
        _aws_command(arguments, config),
        _aws_environment(config),
    )
