import logging
import sleekxmpp

import Processor

class EchoBot(sleekxmpp.ClientXMPP):
    def __init__(self, opts):
        self._folder = opts.folder;
        sleekxmpp.ClientXMPP.__init__(self, opts.jid, opts.password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        body = msg["body"]
        parts = body.split()
        if len(parts) != 2:
            msg.reply("Incorrect command").send()
            return

        if parts[0].lower() == "load":
            try:
                processor = Processor.Processor(self._folder)
                result = processor.ProcessUrl(parts[1])
                msg.reply("\r\n".join(result["urls"] + [result["fullFolder"]])).send()
            except Exception as ex:
                msg.reply("%s" % ex).send()
        else:
            msg.reply("Unknown command").send()


def start(opts):
    if not opts.jid:
        return

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    xmpp = EchoBot(opts)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0004')
    xmpp.register_plugin('xep_0060')
    xmpp.register_plugin('xep_0199')

    if opts.proxy_host:
        xmpp.use_proxy = True
        xmpp.proxy_config = {
            'host': opts.proxy_host,
            'port': int(opts.proxy_port),
            'username': opts.proxy_user,
            'password': opts.proxy_pass}

    if xmpp.connect():
        xmpp.process()
        print("Started")
    else:
        print("Unable to connect.")
