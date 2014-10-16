from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

import Processor

class MainHandler(RequestHandler):
    def get(self):
        self.write("ImgLoader")

class DownloadHandler(RequestHandler):
    def get(self, url):
        processor = Processor.Processor(self.application.settings["folder"])
        result = processor.ProcessUrl(url)
        for url in result["urls"]:
            self.write("%s<br/>" % url)
        self.write(result["fullFolder"])

def start(opts):
    application = Application([
        url(r"/", MainHandler),
        url(r"/download/(.*)", DownloadHandler, name="download")
    ])
    application.settings["folder"] = opts.folder;
    application.listen(9356)
    IOLoop.instance().start()