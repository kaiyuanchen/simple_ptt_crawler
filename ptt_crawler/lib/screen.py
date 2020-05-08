import logging
import re


class Screen:
    def __init__(self):
        self.__screen = []
        self.__clear_screen()
        self.__current_cursor = {'x': 0, 'y': 0}

    def __clear_screen(self):
        self.__screen = [[' ' for y in range(100)] for x in range(24)]

    def __clear_line(self, i):
        self.__screen[i] = [' ' for y in range(100)]

    def __remove_firstline(self):
        self.__screen.pop(0)
        self.__screen.append([' ' for y in range(100)])

    def __update_cursor(self, x, y):
        self.__current_cursor['x'] = x
        self.__current_cursor['y'] = y

    def __backspace(self):
        x = self.__current_cursor['x'] = self.__current_cursor['x'] - 1
        y = self.__current_cursor['y']
        self.__screen[y][x] = ""

    def __render_code(self, code):

        # clear screen
        if code == '2J':
            self.__clear_screen()
            self.__update_cursor(0, 0)

        # move cursor x,y
        elif "H" in code:
            if code == "H":
                self.__update_cursor(0, 0)
            else:
                code = code.replace('H', '')
                y, x = code.split(';')
                self.__update_cursor(int(x) - 1, int(y) - 1)

        # clear line
        elif code == 'K':
            x = self.__current_cursor['x']
            y = self.__current_cursor['y']
            tmp = self.__screen[y][:x]
            self.__clear_line(y)
            self.__screen[y][:x] = tmp

    def __render_text(self, text: str) -> None:
        x = self.__current_cursor['x']
        y = self.__current_cursor['y']
        buf = []
        for word in text:
            if word == '\x08':  # backspace
                if len(buf) > 0:
                    buf.pop()
                else:
                    self.__backspace()
                continue

            buf.append(word)
            if re.match("([^\x00-\xff]+)", word, re.I):
                buf.append('')

        self.__screen[y][x:x + len(buf)] = buf
        self.__update_cursor(x + len(buf), y)

    def render(self, input: str) -> str:
        text_buf = ''
        code_buf = ''
        is_code = False  # state

        for word in input:
            if word == '\x1b':
                if text_buf != '':
                    self.__render_text(text_buf)
                    text_buf = ''

                is_code = True
                continue

            elif word == '\n':
                self.__render_text(text_buf)
                if self.__current_cursor['y'] < 23:
                    self.__update_cursor(0, self.__current_cursor['y'] + 1)
                else:
                    self.__remove_firstline()  # if overflow, remove first line
                text_buf = ''
                continue
            elif word == '\r':
                continue

            if is_code:
                if word == '\x5b':  # i == '['
                    continue
                elif word == '\x6d':  # i == 'm'
                    code_buf = code_buf + word
                    is_code = False
                elif word == '\x48' or word == '\x4A':  # i == 'H' or i == 'J'
                    code_buf = code_buf + word
                    is_code = False
                elif word == '\x4B':  # i == 'K'
                    code_buf = code_buf + word
                    is_code = False
                elif word == '\x4D':  # i == 'M'
                    code_buf = code_buf + word
                    is_code = False
                else:
                    code_buf = code_buf + word
                    continue

                # flush code
                self.__render_code(code_buf)
                code_buf = ''
            else:
                text_buf += word

        self.__render_text(text_buf)
        return self.get_screen(0, len(self.__screen))

    def get_screen(self, start, limit) -> str:
        lines = []

        try:
            for i in range(start, start + limit):
                lines.append("".join(self.__screen[i]))
        except Exception as e:
            logging.error(e)
            lines = []

        return "\n".join(lines)
