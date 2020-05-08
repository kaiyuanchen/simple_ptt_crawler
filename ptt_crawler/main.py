"""
Usage:
  this.py  --out=<arg> --log_conf=<arg> --conf=<arg>

Options:
  -h --help         Show this screen.
  --out=<arg>
  --log_conf=<arg>
  --conf=<arg>
"""

from docopt import docopt
from lib.client import TelnetClient
from lib.command import Command
import configparser
import logging.config
import sys

if __name__ == '__main__':
    arguments = docopt(__doc__)
    log_conf_src = arguments['--log_conf']
    conf_src = arguments['--conf']
    outpath = arguments['--out']

    logging.config.fileConfig(fname=log_conf_src)

    cfg = configparser.ConfigParser()
    cfg.read(conf_src)

    username = cfg['USER']['name']
    password = cfg['USER']['password']
    board = cfg['CRAWL']['board']
    index = int(cfg['CRAWL']['index'])

    telnet_client = TelnetClient()
    telnet_client.start()
    ptt_cmd = Command(telnet_client)
    ptt_cmd.login(username, password)
    article = ptt_cmd.get_article(board, index)
    telnet_client.close()

    with open(outpath, 'a') as out_file:
        out_file.write(article)