from video import Video
from threading import Thread
from queue import SimpleQueue
from sanitize_filename import sanitize
from pathlib import Path
from time import sleep


class Manager:
    def __init__(self):
        self.video_list: list[Video] = []
        self.bvid_set = set()
        self.queue = SimpleQueue()
        self.path = ""

    def get_info_worker(self):
        while not self.queue.empty():
            video: Video = self.queue.get()
            video.get_info()
            sleep(1)

    def add_videos_by_number(self, video_numbers: list[str]):
        for video_number in video_numbers:
            try:
                video = Video(video_number)
            except:
                continue
            if (bvid := video.v.get_bvid()) not in self.bvid_set:
                self.bvid_set.add(bvid)
                self.video_list.append(video)
                self.queue.put(video)
        Thread(target=self.get_info_worker).start()

    def download_worker(self, parent_dir: Path):
        while not self.queue.empty():
            video: Video = self.queue.get()
            filename = sanitize(video.title) + ".m4a"
            while True:
                try:
                    video.download(parent_dir / filename)
                    break
                except:
                    sleep(1)
            sleep(1)

    def download(self):
        parent_dir = Path(self.path)
        for video in self.video_list:
            self.queue.put(video)
        Thread(target=self.download_worker, args=(parent_dir,)).start()

    def get_progress(self):
        return [
            {
                "number": v.number,
                "title": v.title,
                "received": v.received_bytes,
                "total": v.length,
            }
            for v in self.video_list
        ]
