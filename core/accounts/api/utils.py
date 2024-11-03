import threading


class EmailThread(threading.Thread):
    def __init__(self, email_obj):
        self.email_obj = email_obj
        threading.Thread.__init__(self)

    def run(self):
        self.email_obj.send()