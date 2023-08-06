from .exceptions import *
from bilibili_api import video, sync
from httpx import stream
from os import PathLike

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Referer": "https://www.bilibili.com",
}


class Video:
    def __init__(self, video_number: str):
        self.title = None
        self.received_bytes = 0
        self.length = 0
        video_number = video_number.strip()
        if len(video_number) <= 2:
            raise InvalidVideoNumberException(
                f"The video number {video_number} is too short!"
            )
        if video_number[:2].upper() == "AV":
            if not video_number[2:].isnumeric():
                raise InvalidVideoNumberException(
                    f"Invalid AV video number {video_number}!"
                )
            else:
                self.number = "AV" + video_number[2:]
                self.v = video.Video(aid=int(video_number[2:]))
                return
        if video_number[:2].upper() != "BV":
            raise InvalidVideoNumberException(f"Invalid video number {video_number}!")
        else:
            self.number = "BV" + video_number[2:]
            self.v = video.Video(bvid=self.number)

    def get_info(self):
        try:
            info = sync(self.v.get_info())
        except:
            raise BiliBiliAPIException("Error happens with bilibili-api-python.")
        self.title = info["title"]

    def get_url(self):
        try:
            download_url_data = sync(self.v.get_download_url(0))
            detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
            streams = detecter.detect_best_streams()
        except:
            raise BiliBiliAPIException("Error happens with bilibili-api-python.")
        if detecter.check_flv_stream() == True:
            raise BadVideoException(
                f"This video ({self.title})) is only available in flv format."
            )
        return streams[1].url

    def download(self, file: int | str | bytes | PathLike):
        with stream("GET", self.get_url(), headers=HEADERS) as r:
            self.length = int(r.headers["content-length"])
            self.received_bytes = 0
            with open(file, "wb") as f:
                for chunk in r.iter_bytes(1024):
                    if not chunk:
                        break
                    self.received_bytes += len(chunk)
                    f.write(chunk)
