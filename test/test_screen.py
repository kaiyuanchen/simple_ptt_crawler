import unittest
from unittest import TestCase
from ptt_crawler.lib.client import TelnetClient


class TestClient(TestCase):
    def test_run(self):
        TelnetClient()
        self.assertTrue(True)