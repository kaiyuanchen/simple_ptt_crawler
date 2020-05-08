from unittest import TestCase

from ptt_crawler.lib.screen import Screen


class TestScreen(TestCase):
    def test_render(self):
        screen = Screen()
        content = screen.render("aaa\nbbb")
        self.assertEqual(content.rsplit(), ['aaa', 'bbb'])
