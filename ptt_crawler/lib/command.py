import logging
import re

from .client import Client
from .key import ScreenKeyword, CommandKey


class Command:

    _login_status = False

    def __init__(self, client: Client):
        self.__client = client

    def login(self, user_id: str, user_pwd: str) -> None:
        if self._login_status:
            logging.info("you are already logged in")
            return

        logging.info("login user: {}".format(user_id))
        self.__client.submit("{}\r\n".format(user_id))
        curr_content = self.__client.submit("{}\r\n".format(user_pwd))

        while any(key in curr_content for key in ScreenKeyword.logins):
            if ScreenKeyword.login_multi in curr_content:
                logging.info("accept multi login...")
                curr_content = self.__client.submit(CommandKey.No)
            elif ScreenKeyword.login_error in curr_content:
                logging.info("delete login error...")
                curr_content = self.__client.submit(CommandKey.Yes)
            elif ScreenKeyword.any in curr_content:
                curr_content = self.__client.submit(CommandKey.Enter)

        if ScreenKeyword.menu in curr_content:
            logging.info("login success ^^")

    def get_article(self, board: str, index: int) -> str:
        self.__get_board(board)
        self.__client.submit(str(index) + CommandKey.Enter)
        self.__client.submit(CommandKey.Right)

        lines = []
        while True:
            footer = self.__client.get_footer()

            match_artice_footer = \
                re.search(
                    "".join(ScreenKeyword.article_position),
                    footer,
                    re.I)
            match_anime = re.search(ScreenKeyword.animation, footer, re.I)

            if match_anime:
                logging.info("this article is an animation")
                return ""

            if not match_artice_footer:
                logging.error("cant parse this article")
                raise Exception('index: {}, cant parse progress'.format(index))

            progress = int(match_artice_footer.groups()[1])
            start_line = int(match_artice_footer.groups()[2])

            if start_line == 1:  # adjust the index of first page
                start_line = 0

            content = self.__client.get_screen(0, 23)
            curr_lines = content.split("\n")

            lines[start_line:] = curr_lines

            if progress == 100:
                break

            self.__client.go_next_page()
        return "\n".join(lines)

    def __get_board(self, board):
        self.__go_main_menu()
        self.__client.submit("s")
        curr_content = self.__client.submit(board + CommandKey.Enter)
        curr_content_lines = curr_content.split("\n")

        if re.search(ScreenKeyword.any, curr_content_lines[-1], re.I):
            curr_content = self.__client.submit(CommandKey.Enter)

        return curr_content

    def __go_main_menu(self):
        while True:
            header = self.__client.get_header()
            if re.search(ScreenKeyword.menu, header, re.I):
                break
            else:
                self.__client.submit(CommandKey.Left)
