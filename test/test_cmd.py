from unittest import TestCase
from unittest import mock
from ptt_crawler.lib.command import Command


class TestCommand(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCommand, self).__init__(*args, **kwargs)
        self.__mock_client = mock.MagicMock()
        self.__command = Command(self.__mock_client)

    def test_login(self):
        self.__command.login("aaa", "bbb")
        self.assertEqual(
            self.__mock_client.submit.call_args_list[0],
            mock.call('aaa\r\n'))
        self.assertEqual(
            self.__mock_client.submit.call_args_list[1],
            mock.call('bbb\r\n'))
        self.__mock_client.submit.reset_mock()
