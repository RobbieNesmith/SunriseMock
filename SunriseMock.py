import threading
import tkinter as tk
from bottle import request, route, run

WAITING_FOR_FADE = 0
FADING = 1
MANUAL_MODE = 2
SUNSET_MODE = 3


class Preview(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()


previewWindow = Preview()

previewWindow.master.title("SunriseMock Preview")
previewWindow.master.geometry("400x400")
previewWindow.master["bg"] = "black"


def rgbw2rgb(color):
    return {
        "red": min(255, max(color["red"] + color["white"], 0)),
        "green": min(255, max(color["green"] + color["white"], 0)),
        "blue": min(255, max(color["blue"] + color["white"], 0))
    }


def color2hex(color):
    return f"#{color['red']:02x}{color['green']:02x}{color['blue']:02x}"


context = {"state": WAITING_FOR_FADE}

manual_color = {"red": 0, "green": 0, "blue": 0, "white": 0}


@route("/manual")
def manual():
    context["state"] = MANUAL_MODE
    if "red" in request.query:
        manual_color["red"] = int(request.query["red"])

    if "green" in request.query:
        manual_color["green"] = int(request.query["green"])

    if "blue" in request.query:
        manual_color["blue"] = int(request.query["blue"])

    if "white" in request.query:
        manual_color["white"] = int(request.query["white"])

    previewWindow.master["bg"] = color2hex(rgbw2rgb(manual_color))

    return "200 OK"


def start_server():
    run(host="0.0.0.0", port=8000)


server_thread = threading.Thread(target=start_server)
server_thread.start()
previewWindow.mainloop()
server_thread.join()
