from threading import Timer
import time


class PatriotTask:
    def __init__(self, name, target, interval, **kwargs):
        self.pt_thread = None

        self.name = name
        self.kwargs = kwargs
        self.target = target
        self.interval = interval
        self.run_count = 0
        self.to_run = kwargs.get('run', True)
        self.func_cb = kwargs.get('callback', None)
        self.target_args = kwargs.get('targetArgs', None)
        self.func_cb_args = kwargs.get('callbackArgs', None)
        self.continue_for = kwargs.get('rounds', -1)

    def run(self):
        if self.to_run:
            if self.continue_for == -1 or self.run_count <= self.continue_for:
                self.pt_thread = Timer(0, self.target_handler)
                self.pt_thread.start()

    def stop(self):
        if self.is_running():
            self.to_run = False
            self.pt_thread.cancel()

    def target_handler(self):
        if self.target_args is not None:
            self.target(self.target_args)
        else:
            self.target()

        if self.func_cb is not None:
            self.func_cb(self.func_cb_args)

        self.run_count += 1
        time.sleep(self.interval)
        self.run()

    def is_running(self):
        return self.pt_thread is not None and self.pt_thread.is_alive()
