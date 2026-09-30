from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from squid.constants import Environment
from squid.resources import s3 as s3_resources


class S3ResourcesTest(unittest.TestCase):
    def test_on_premises_rustfs_uses_mounted_ca_certificate(self) -> None:
        with (
            patch.object(s3_resources, "env", Environment.ON_PREMISES),
            patch.object(s3_resources, "is_databricks", return_value=False),
            patch.dict(
                os.environ,
                {
                    "RUSTFS_ACCESS_KEY_ID": "access-key",
                    "RUSTFS_SECRET_ACCESS_KEY": "secret-key",
                },
                clear=True,
            ),
        ):
            config = s3_resources.get_s3_config()

        self.assertEqual("https://rustfs:9000", config.endpoint_url)
        self.assertEqual("/etc/rustfs/tls/ca.crt", config.verify)


if __name__ == "__main__":
    unittest.main()
