from bottle import request, response, Bottle, static_file
from manager import Manager
from json import dumps
import webview

manager = Manager()
app = Bottle()


@app.get("/")
def frontend():
    return static_file("index.html", root="frontend/dist")


@app.get("/<filepath:path>")
def frontend(filepath):
    return static_file(filepath, root="frontend/dist")


@app.post("/video")
def add_videos():
    nvlist = request.json["nvlist"].split()
    manager.add_videos_by_number(nvlist)
    return "OK"


@app.get("/progress")
def get_progress():
    response.content_type = "application/json"
    return dumps(manager.get_progress())


@app.get("/download")
def download():
    manager.download()
    return "OK"


@app.get("/path")
def get_path():
    result = webview.active_window().create_file_dialog(
        dialog_type=webview.FOLDER_DIALOG
    )
    if result:
        manager.path = result[0]
    return manager.path
