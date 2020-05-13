from unittest import TestCase
from unittest import mock

from ptt_crawler.lib.key import ScreenKeyword
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

    def test_get_article(self):
        self.__mock_client.get_header.return_value = ScreenKeyword.menu
        self.__mock_client.submit.return_value = ScreenKeyword.any
        self.__mock_client.submit.return_value = ScreenKeyword.any
        self.__mock_client.get_footer.return_value = \
            "瀏覽 第 1/1 頁 (100%)  目前顯示: 第 01~19 行  (y)回應(X%)推文(h)說明(←)離開"
        self.__mock_client.get_screen.return_value = "1234\n5678"
        self.assertEqual(self.__command.get_article("aaa", 1), "1234\n5678")
