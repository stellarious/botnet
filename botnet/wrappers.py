from threading import Thread
from .modules import BaseModule
from .logging import get_logger


class ModuleWrapper(object):

    def __init__(self, module):
        self.module = module
        self.thread = None
        self.logger = get_logger(str(self))
        super(ModuleWrapper, self).__init__()

    def __str__(self):
        return '%s: %s' % (self.__class__.__name__, self.module)

    def is_alive(self):
        # If a module is not a BaseModule instance it is an BaseIdleModule which
        # dosn't use a thread
        if not isinstance(self.module, BaseModule):
            return True
        return self.thread and self.thread.is_alive()

    def start(self):
        self.logger.debug('Start')
        if not self.is_alive():
            self.thread = Thread(target=self.module.run)
            self.thread.start()

    def stop(self):
        self.logger.debug('Stop')
        if self.thread:
            self.module.stop()
            self.thread.join()