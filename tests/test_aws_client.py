"""Rules: no creds -> honest mock; env creds + stubs -> green probes; receipts redact & survive."""

import os
import tempfile
import unittest
from unittest import mock

from backend.aws import client, receipts


class _FakeDynamo:
    def list_tables(self):
        return {"TableNames": ["route_trips"]}


class _FakeLambda:
    def list_functions(self, MaxItems=1):
        return {"Functions": []}


class _FakeBedrock:
    def list_foundation_models(self):
        return {"modelSummaries": []}


def _fake_factory(name):
    return {"dynamodb": _FakeDynamo(), "lambda": _FakeLambda(), "bedrock": _FakeBedrock()}[name]


_AWS_ENV = ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_PROFILE", "ECOROUTE_AWS_MODE")


class AwsClientRules(unittest.TestCase):
    def setUp(self):
        client._factory = None
        self._stash = {k: os.environ.pop(k, None) for k in _AWS_ENV}

    def tearDown(self):
        for key, value in self._stash.items():
            os.environ.pop(key, None)
            if value is not None:
                os.environ[key] = value

    def test_no_creds_means_mock_with_none_probes(self):
        state = client.aws_state()
        self.assertEqual(state["mode"], "mock")
        self.assertIsNone(state["probe"]["dynamodb_ok"])
        self.assertIsNone(state["probe"]["lambda_ok"])
        self.assertIsNone(state["probe"]["bedrock_ok"])
        self.assertIn(".env", state["reason"])

    def test_env_creds_with_stubbed_factory_go_live_green(self):
        client._factory = _fake_factory
        os.environ["AWS_ACCESS_KEY_ID"] = "AKIATEST"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "not-a-real-key"
        state = client.aws_state()
        self.assertEqual(state["mode"], "live")
        self.assertTrue(state["probe"]["dynamodb_ok"])
        self.assertTrue(state["probe"]["lambda_ok"])
        self.assertTrue(state["probe"]["bedrock_ok"])

    def test_no_boto3_never_crashes(self):
        client._factory = None
        os.environ["AWS_ACCESS_KEY_ID"] = "AKIATEST"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "not-a-real-key"
        state = client.aws_state()  # boto3 is absent in this environment
        self.assertEqual(state["mode"], "live")
        self.assertTrue(all(v is False for v in state["probe"].values()))
        self.assertTrue(state["reason"])  # some explanation, never a crash


class ReceiptRules(unittest.TestCase):
    def test_secrets_masked_before_write(self):
        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.object(receipts, "RECEIPTS_DIR", folder):
                self.assertTrue(receipts.record(
                    "probe",
                    {"trip": "rohini->pitampura", "aws_secret": "S3CR3T",
                     "session_token": "T0K3N", "api_key": "K3Y"},
                ))
                blocks = os.listdir(folder)
                self.assertEqual(len(blocks), 1)
                data = open(os.path.join(folder, blocks[0]), encoding="utf-8").read()
                self.assertIn("rohini", data)
                for leak in ("S3CR3T", "T0K3N", "K3Y"):
                    self.assertNotIn(leak, data)

    def test_creates_missing_dir_and_tail_reads_back(self):
        base = tempfile.mkdtemp()
        target = os.path.join(base, "one", "two", "receipts")
        before = [r["payload"] for r in receipts.tail(50)]
        self.assertNotIn({"a": 1}, before)  # temp patch is isolated from the real ledger
        with mock.patch.object(receipts, "RECEIPTS_DIR", target):
            self.assertTrue(receipts.record("t", {"a": 1}))
            self.assertTrue(os.path.isdir(target))
            self.assertEqual(receipts.tail(1)[0]["payload"], {"a": 1})

    def test_nested_dicts_are_redacted_too(self):
        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.object(receipts, "RECEIPTS_DIR", folder):
                receipts.record("n", {"src": {"db_secret": "NESTLE"}})
                data = open(os.path.join(folder, os.listdir(folder)[0]), encoding="utf-8").read()
                self.assertNotIn("NESTLE", data)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
