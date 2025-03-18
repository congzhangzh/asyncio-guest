from asyncio_guest_run import asyncio_guest_run, schedule_on_asyncio
import asyncio_example_tasks

import sys
import traceback

from PySide6 import QtCore, QtWidgets
from outcome import Error

REENTER_EVENT_TYPE = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

class ReenterEvent(QtCore.QEvent):
    pass

class Reenter(QtCore.QObject):
    def event(self, event):
        event.fn()
        return False

class QtHost:
    def __init__(self, app):
        self.app = app
        self.reenter = Reenter()

    def run_sync_soon_threadsafe(self, fn):
        event = ReenterEvent(REENTER_EVENT_TYPE)
        event.fn = fn
        self.app.postEvent(self.reenter, event)

    def done_callback(self, outcome):
        print(f"Outcome: {outcome}")
        if isinstance(outcome, Error):
            exc = outcome.error
            traceback.print_exception(type(exc), exc, exc.__traceback__)
        self.app.quit()

    def mainloop(self):
        self.app.exec()  # PySide6使用exec()代替exec_()

class QtDisplay:
    def __init__(self, app):
        self.app = app
        self.widget = QtWidgets.QProgressDialog("Fetching...", "Cancel", 0, 0)
        self.widget.setMinimumDuration(0)

    def set_title(self, title):
        self.widget.setLabelText(title)

    def set_max(self, maximum):
        self.widget.setMaximum(maximum)

    def set_value(self, downloaded):
        self.widget.setValue(downloaded)

    def set_cancel(self, fn):
        self.widget.canceled.connect(fn)
        self.app.lastWindowClosed.connect(fn)

def main(task):
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    host = QtHost(app)
    display = QtDisplay(app)
    asyncio_guest_run(
        task,
        display,
        run_sync_soon_threadsafe=host.run_sync_soon_threadsafe,
        run_sync_soon_not_threadsafe=None,
        done_callback=host.done_callback,
    )
    host.mainloop()

if __name__ == '__main__':
    main(asyncio_example_tasks.count) 