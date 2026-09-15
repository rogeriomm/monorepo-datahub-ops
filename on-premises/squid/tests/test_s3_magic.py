from __future__ import annotations

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

from squid.jupyter import s3 as s3_magic
from squid.resources.s3 import S3Config


class S3MagicTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = S3Config(
            endpoint_url="https://seaweedfs:8333",
            aws_access_key_id="access-key",
            aws_secret_access_key="secret-key",
            region_name="us-east-1",
            verify="/certificates/ca.crt",
        )
        self.get_config = patch.object(
            s3_magic,
            "get_s3_config",
            return_value=self.config,
        )
        self.mock_get_config = self.get_config.start()
        self.addCleanup(self.get_config.stop)

    @staticmethod
    def process(output: str = "", return_code: int = 0) -> Mock:
        process = Mock()
        process.stdout = io.StringIO(output)
        process.wait.return_value = return_code
        return process

    def test_forwards_quoted_arguments_to_aws_s3(self) -> None:
        process = self.process("2026-09-14 bucket\n")
        with patch.object(s3_magic.subprocess, "Popen", return_value=process) as popen:
            output = io.StringIO()
            with redirect_stdout(output):
                s3_magic.run_s3("ls 's3://lakehouse/a directory/' --recursive")

        self.assertEqual("2026-09-14 bucket\n", output.getvalue())
        command = popen.call_args.args[0]
        self.assertEqual(
            [
                "aws",
                "--endpoint-url",
                "https://seaweedfs:8333",
                "--region",
                "us-east-1",
                "--ca-bundle",
                "/certificates/ca.crt",
                "s3",
                "ls",
                "s3://lakehouse/a directory/",
                "--recursive",
            ],
            command,
        )
        environment = popen.call_args.kwargs["env"]
        self.assertEqual("access-key", environment["AWS_ACCESS_KEY_ID"])
        self.assertEqual("secret-key", environment["AWS_SECRET_ACCESS_KEY"])
        self.assertEqual("", environment["AWS_PAGER"])

    def test_disables_ssl_verification_when_configured(self) -> None:
        config = S3Config(
            endpoint_url="https://example.test",
            aws_access_key_id=None,
            aws_secret_access_key=None,
            region_name=None,
            verify=False,
        )
        self.mock_get_config.return_value = config
        with patch.object(
            s3_magic.subprocess,
            "Popen",
            return_value=self.process(),
        ) as popen:
            s3_magic.run_s3("ls")

        self.assertEqual(
            [
                "aws",
                "--endpoint-url",
                "https://example.test",
                "--no-verify-ssl",
                "s3",
                "ls",
            ],
            popen.call_args.args[0],
        )

    def test_static_credentials_do_not_inherit_a_session_token(self) -> None:
        with patch.dict(os.environ, {"AWS_SESSION_TOKEN": "temporary"}):
            environment = s3_magic._aws_environment(self.config)
        self.assertNotIn("AWS_SESSION_TOKEN", environment)

    def test_reports_a_nonzero_aws_cli_status(self) -> None:
        with (
            patch.object(
                s3_magic.subprocess,
                "Popen",
                return_value=self.process("failure\n", return_code=2),
            ),
            redirect_stdout(io.StringIO()),
        ):
            with self.assertRaisesRegex(s3_magic.S3MagicError, "status 2"):
                s3_magic.run_s3("mb s3://scratch")

    def test_reports_a_missing_aws_cli(self) -> None:
        with patch.object(
            s3_magic.subprocess,
            "Popen",
            side_effect=FileNotFoundError,
        ):
            with self.assertRaisesRegex(s3_magic.S3MagicError, "not installed"):
                s3_magic.run_s3("ls")

    def test_rejects_invalid_shell_quoting_before_starting_aws(self) -> None:
        with patch.object(s3_magic.subprocess, "Popen") as popen:
            with self.assertRaisesRegex(s3_magic.S3MagicError, "Invalid command line"):
                s3_magic.run_s3("ls 'unterminated")
        popen.assert_not_called()


if __name__ == "__main__":
    unittest.main()
