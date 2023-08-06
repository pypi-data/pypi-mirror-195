"""\
Purpose: Visualize test scenarios
Initial Version: Costas Skarakis 12/20/2021  
"""

import tkinter.tix as gr
import threading
from sip.SipEndpoint import SipEndpoint

MAXROWS = 40


class LoadWindow:
    def __init__(self):
        self.root = gr.Tk()
        scroll_window = gr.ScrolledWindow(self.root, width=300, height=800, scrollbar=gr.AUTO)
        scroll_window.pack(expand=1, fill=gr.BOTH)
        self.window = scroll_window.window
        self.subs = {}

    def paint(self, number):
        if number not in self.subs:
            count = len(self.subs)
            sub_row = count % MAXROWS
            sub_col = count // MAXROWS
            frame = gr.Frame(self.window)
            frame.grid(row=sub_row, column=sub_col)
            frame.label = gr.Label(frame, text=number, width=13)
            frame.arrow = gr.Label(frame, width=3, bg="yellow")
            frame.message = gr.Label(frame, width=30)
            frame.label.pack(side=gr.LEFT)
            frame.arrow.pack(side=gr.LEFT)
            frame.message.pack(side=gr.LEFT)
            self.subs[number] = frame

    def arrow(self, number, text):
        self.subs[number].arrow["text"] = text

    def message(self, number, text):
        self.subs[number].message["text"] = text

    def start(self, func_on_thread, *args, **kwargs):
        func_thread = threading.Thread(target=func_on_thread, args=args, kwargs=kwargs).start()
        self.root.mainloop()
        print("Exit main loop")
        func_thread.join()


class SipEndpointView(SipEndpoint):
    def __init__(self, view, number):
        self.view = view
        super().__init__(number)

    def connect(self, *args, **kwargs):
        self.view.paint(self.number)
        super().connect(*args, **kwargs)

    def use_link(self, *args, **kwargs):
        self.view.paint(self.number)
        super().use_link(*args, **kwargs)

    def send(self, *args, **kwargs):
        self.view.arrow(self.number, "Sndg")
        message = super().send(*args, **kwargs)
        self.view.arrow(self.number, "Sent")
        self.view.message(self.number, message.get_status_or_method())
        return message

    def reply(self, *args, **kwargs):
        self.view.arrow(self.number, "Sndg")
        message = super().reply(*args, **kwargs)
        self.view.arrow(self.number, "Sent")
        self.view.message(self.number, message.get_status_or_method())
        return message

    def send_new(self, *args, **kwargs):
        self.view.arrow(self.number, "Sndg")
        message = super().send_new(*args, **kwargs)
        self.view.arrow(self.number, "Sent")
        self.view.message(self.number, message.get_status_or_method())
        return message

    def wait_for_message(self, message_type, **kwargs):
        self.view.arrow(self.number, "Wng")
        self.view.message(self.number, message_type)
        message = super().wait_for_message(message_type, **kwargs)
        self.view.arrow(self.number, "Rcvd")
        self.view.message(self.number, message.get_status_or_method())
        return message

    def colour(self, colour):
        self.view.subs[self.number].arrow["bg"] = colour

    def update_text(self, text=""):
        self.view.message(self.number, text)

    def update_arrow(self, arrow=""):
        self.view.arrow(self.number, arrow)

    def make_busy(self, busy=True):
        super().make_busy(busy)
        self.colour(["yellow", "cyan"][busy])
