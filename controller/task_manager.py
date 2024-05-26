import functools

from PyQt6.QtCore import QObject, pyqtProperty as Property, QThreadPool, QMutex, QRunnable, QMutexLocker, QThread, \
    QTimer
from PyQt6.QtCore import pyqtSignal as Signal, pyqtSlot as Slot


class TaskManager(QObject):

    def __init__(self):
        super().__init__()
        self.task_pool = QThreadPool(self)
        # The controller cannot run multiple tasks in parallel
        # because most of the tasks use the same data as model, serial port access etc.
        # (have a critical section).
        # All backend tasks should be run in a single thread sequentially but
        # that thread must be separated from the thread of GUI.
        self.task_pool.setMaxThreadCount(1)
        self.task_mutex = QMutex()


class TaskRunner(QRunnable):

    def __init__(self, task_manager: TaskManager, task: callable, *args, **kwargs):
        """
        This class is used to run functions of Controller in the thread separated from GUI.

        :param task_manager: the instance of the TaskManager class.
        :param task: the function of the controller that should be run in background.
        :param args: positional arguments of the task.
        :param kwargs: named arguments of the task.
        """
        super().__init__()
        self.task_manager = task_manager
        self.task = task
        self.result = TaskResult(task_manager)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        with QMutexLocker(self.task_manager.task_mutex):
            self.result.result = self.task(self.task_manager, *self.args, **self.kwargs)
        self.result.status = True


class TaskResult(QObject):
    status_changed = Signal(bool)
    result_changed = Signal('QVariant')

    def __init__(self, parent=None):
        super().__init__(parent)
        self._status = False
        self._result = None

    @Property(bool, notify=status_changed)
    def status(self) -> bool:
        return self._status

    @status.setter
    def status(self, new_value: bool):
        self._status = new_value
        self.status_changed.emit(new_value)

    @Property('QVariant', notify=result_changed)
    def result(self):
        return self._result

    @result.setter
    def result(self, new_value):
        if new_value is not None:
            self._result = new_value
            self.result_changed.emit(new_value)


def background_task(task):
    """
    This decorator is used to run functions of the Controller class in the thread separated from GUI.
    """

    @functools.wraps(task)
    def task_wrapper(task_manager, *args, **kwargs):
        if task_manager.task_pool.contains(QThread.currentThread()):
            # NOTE:
            #   If one background task is called from another background task,
            #   run it immediately without using the task pool.
            return task(task_manager, *args, **kwargs)
        task_runner = TaskRunner(task_manager, task, *args, **kwargs)
        task_manager.task_pool.start(task_runner)
        return task_runner.result

    return task_wrapper



