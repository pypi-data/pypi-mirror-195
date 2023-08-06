from multiprocessing import Process

from eipiphany_core.framework.base.source import Source


class SedaSource(Source):

  def __init__(self, queue, configuration):
    self.__queue = queue
    self.__concurrent_consumers = configuration.concurrent_consumers
    self.__source_wrapper = None

  def set_source_wrapper(self, source_wrapper):
    self.__source_wrapper = source_wrapper

  def start(self):
    consumer_process = []
    for i in range(self.__concurrent_consumers):
      p = Process(target=self.__source_wrapper.wait_for_events)
      p.daemon = True
      p.start()
      consumer_process.append(p)
    return consumer_process

  def wait_for_event(self):
    return self.__queue.get()

  def event_success(self, exchange):
    self.__queue.task_done()
    pass

  def event_failure(self, err, exchange):
    self.__queue.task_done()
    pass

