import urllib2
import os
from bs4 import BeautifulSoup
from urlparse import urlparse

class Processor:
    def __init__(self, folder):
        self._folder = folder

    def ProcessUrl(self, url):
        id = self.ParseId(url)
        urls = self.ParsePage(url, id)
        fullFolder = self.DownloadUrls(urls, id)
        return dict(fullFolder = fullFolder, urls = urls)

    def ParseId(self, url):
        path = urlparse(url).path
        pathPart = path.split("/").pop()
        id = int(pathPart.split("-")[0])
        return id

    def ParsePage(self, url, id):
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html)
        divContainer = soup.find("div", {"id": "news-id-%i" % id})
        images = divContainer.find_all("img")
        result = [x.attrs["src"] for x in images]
        return result

    def DownloadUrls(self, urls, id):
        fullFolder = os.path.join(self._folder, str(id))
        if not os.path.exists(fullFolder):
            os.mkdir(fullFolder)
        for url in urls:
            print(url)
            local = os.path.join(fullFolder + "/", os.path.basename(url))
            if not os.path.exists(local):
                f = urllib2.urlopen(url)
                with open(local, "wb") as local_file:
                    local_file.write(f.read())
        return fullFolder
