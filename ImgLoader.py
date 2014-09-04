import urllib2
import os
from bs4 import BeautifulSoup
from urlparse import urlparse
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url

def ParseId(url):
    path = urlparse(url).path
    pathPart = path.split("/").pop()
    id = int(pathPart.split("-")[0])
    return id

def ParsePage(url, id):
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html)
    divContainer = soup.find("div", {"id": "news-id-%i" % id})
    images = divContainer.find_all("img")
    result = [x.attrs["src"] for x in images]
    return result

def DownloadUrls(urls, id):
    if not os.path.exists(str(id)):
        os.mkdir(str(id))
    for url in urls:
        print(url)
        local = "%i/%s" % (id, os.path.basename(url))
        if not os.path.exists(local):
            f = urllib2.urlopen(url)
            with open(local, "wb") as local_file:
                local_file.write(f.read())

def ProcessUrl(url):
    id = ParseId(url)
    urls = ParsePage(url, id)
    DownloadUrls(urls, id)
    return urls

class DownloadHandler(RequestHandler):
    def get(self, url):
        urls = ProcessUrl(url)
        for url in urls:
            self.write("%s<br/>" % url)

application = Application([
    url(r"/download/(.*)", DownloadHandler, name="download")
])

if __name__ == "__main__":
    application.listen(9356)
    IOLoop.instance().start()