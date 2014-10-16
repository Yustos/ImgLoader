import CommandBot
import CommandWeb
import Processor

import logging
from optparse import OptionParser

def getOptions():
    optp = OptionParser()
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    optp.add_option("-f", "--folder", dest="folder", help="Folder to store files")

    optp.add_option("-j", "--jid", dest="jid", help="JID to use")
    optp.add_option("-p", "--password", dest="password", help="password to use")
    optp.add_option("--phost", dest="proxy_host", help="Proxy hostname")
    optp.add_option("--pport", dest="proxy_port", help="Proxy port")
    optp.add_option("--puser", dest="proxy_user", help="Proxy username")
    optp.add_option("--ppass", dest="proxy_pass", help="Proxy password")

    opts, args = optp.parse_args()
    return opts

if __name__ == "__main__":
    opts = getOptions()
    CommandBot.start(opts)
    CommandWeb.start(opts)
