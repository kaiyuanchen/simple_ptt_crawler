import telnetlib
import time
import logging
from abc import abstractmethod
from .screen import Screen
from .exception import GetScreenLimitError
from .key import CommandKey


class Client:
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def submit(self, key: str) -> str:
        pass

    @abstractmethod
    def go_prev_page(self) -> str:
        pass

    @abstractmethod
    def go_next_page(self) -> str:
        pass

    @abstractmethod
    def get_header(self) -> str:
        pass

    @abstractmethod
    def get_footer(self) -> str:
        pass

    @abstractmethod
    def get_screen(self, start: int, limit: int) -> str:
        pass


class TelnetClient(Client):

    def __init__(self):
        self.__screen = Screen()
        self.__telnet = None
        self.__timeout = 5
        self.__enabled = False

    def start(self) -> None:
        if not self.__enabled:
            self.__telnet = telnetlib.Telnet('ptt.cc')
            self.__wait()
            self.__telnet.read_very_eager()

        logging.info("TelnetClient start")

    def close(self):
        self.__telnet.close()

    def submit(self, key: str) -> str:
        logging.debug("submit {}".format(key))
        self.__telnet.write(key.encode('big5'))
        time.sleep(self.__timeout)
        resp = self.__telnet.read_very_eager().decode('big5', 'ignore')
        return self.__screen.render(resp)

    def go_prev_page(self):
        return self.submit(CommandKey.PrevPage)

    def go_next_page(self):
        return self.submit(CommandKey.NextPage)

    def get_header(self) -> str:
        return self.__screen.get_screen(0, 1)

    def get_footer(self) -> str:
        return self.__screen.get_screen(23, 1)

    def get_screen(self, start: int, limit: int) -> str:
        if limit > 23:
            raise GetScreenLimitError()
        return self.__screen.get_screen(start, limit)

    def __wait(self) -> None:
        time.sleep(self.__timeout)
