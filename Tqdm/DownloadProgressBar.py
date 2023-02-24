import requests
from tqdm.auto import tqdm

class DownloadProgressBar:
    """"""
    def __init__(self, url = None, fileName = None):
        self.url = url
        self.fileName = fileName
        if self.fileName is not None:
            self.fileName = fileName
        else:
            self.fileName = self.url.split("/")[-1]
        self.StartDownload(fileName=self.fileName, url=self.url)

    def StartDownload(self, fileName = None, url = None):
        """"""
        response = requests.get(url, stream = True, timeout=(1,2))
        if response.status_code == 200:
            progress = tqdm(desc = fileName, total = int(response.headers.get("content-length", 0)),
                            unit='B', unit_scale=True, unit_divisor=1024,)
            with open(fileName, "wb") as f:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    progress.update(len(data))
            progress.close()

url = 'https://wordnetcode.princeton.edu/2.1/WNsnsmap-2.1.tar.gz'
DownloadProgressBar(url=url)