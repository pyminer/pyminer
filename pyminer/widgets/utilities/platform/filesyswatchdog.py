"""
作者(Author)：1295752786@qq.com
文件系统看门狗-(Watchdog for filesystem)
来源- (source)
https://stackoverflow.com/questions/35874217/watchdog-pythons-library-how-to-send-signal-when-a-file-is-modified
源代码为PyQt4,本人整理、移植到qtpy。(Originally code was in PyQt4 and I transplanted to PySide2.)
"""

from PySide2.QtCore import Signal, QThread, SignalInstance
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileMovedEvent, \
    FileCreatedEvent, FileDeletedEvent
from watchdog.observers import Observer


class MyEventHandler(FileSystemEventHandler, QThread):
    signal_file_modified: SignalInstance = Signal(str)
    signal_file_created: SignalInstance = Signal(str)
    signal_file_deleted: SignalInstance = Signal(str)
    signal_file_moved: SignalInstance = Signal(str, str)  # 仅当在本文件夹内才会触发，如果移动到了其他文件夹则触发删除信号

    def on_deleted(self, event: FileDeletedEvent):
        self.signal_file_deleted.emit(event.src_path)

    def on_modified(self, event: FileModifiedEvent):
        self.signal_file_modified.emit(event.src_path)

    def on_created(self, event: FileCreatedEvent):
        self.signal_file_created.emit(event.src_path)

    def on_moved(self, event: FileMovedEvent):
        self.signal_file_moved.emit(event.src_path, event.dest_path)


class PMGFileSystemWatchdog(QThread):
    """
    Watch Dog 的一切操作都是在path这个文件夹下完成的，其余位置的文件变更并不会被监测到。
    因此，如果将一个文件移动出这个文件夹，触发的并不是“修改”信号，而是触发“删除”信号。

    # TODO 目前仅支持监控一整个文件夹，需要添加监控单一文件的方法
    """

    def __init__(self, path):
        super(PMGFileSystemWatchdog, self).__init__()

        self.path = path
        self.observer = Observer()
        self.event_handler = MyEventHandler()
        self.signal_file_modified: SignalInstance = self.event_handler.signal_file_modified
        self.signal_file_created: SignalInstance = self.event_handler.signal_file_created
        self.signal_file_deleted: SignalInstance = self.event_handler.signal_file_deleted
        self.signal_file_moved: SignalInstance = self.event_handler.signal_file_moved
        self.observer.schedule(self.event_handler, self.path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.deleteLater()
