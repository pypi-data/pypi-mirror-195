__version__ = "0.1.0"

import time
from multiprocessing import Process, Queue
from threading import Timer
from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, TypeVar

from olympipe.pipes.reduce import ReducePipe
from .pipes.generic import GenericPipe
from .pipes.task import TaskPipe
from .pipes.filter import FilterPipe
from .pipes.explode import ExplodePipe
from .pipes.batch import BatchPipe
from .pipes.instance import ClassInstancePipe
from .pipes.timebatch import TimeBatchPipe
from .dispatcher import Dispatcher

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


class Pipeline(Generic[R]):
    max_queue_size: int = 4
    """max_queue_size
    Change this value to alter the maximum number of item per pipeline element. Default
    Default is 4
    """

    @staticmethod
    def get_new_queue() -> "Queue[R]":
        return Queue(maxsize=Pipeline.max_queue_size)

    def __init__(self, datas: Optional[Iterable[R]] = None):
        self._source: "Queue[R]" = Pipeline.get_new_queue()
        self._parents: List["Process"] = []
        self.dispatcher = Dispatcher(self._source)
        self._register(self.dispatcher)
        if datas is not None:
            Timer(0.05, self.source, (datas,)).start()

    def source(self, datas: Iterable[R]) -> None:
        for data in datas:
            self._source.put(data)

        self.auto_close()

    def auto_close(self):
        while not self._source.empty():
            time.sleep(0.15)
        self._source.put(GenericPipe.get_kill_word())

    def _register(self, process: Process):
        """_register
        This method will register a process as parent
        to know when it should stop
        """
        self._parents.append(process)

    def task(self, task: Callable[[R], S], count: int = 1) -> "Pipeline[S]":
        assert count >= 1
        target_queue: "Queue[R]" = Pipeline.get_new_queue()
        output_pipe: "Pipeline[S]" = Pipeline()
        self.dispatcher.dispatch_to([target_queue], count)
        for _ in range(count):
            p = TaskPipe(target_queue, task, output_pipe._source)
            self._register(p)
        return output_pipe

    def class_task(
        self,
        class_constructor: Any,
        class_method: Callable[[Any, R], S],
        class_args: List[Any] = [],
        close_method: Optional[Callable[[Any], Any]] = None,
        class_kwargs: Dict[str, Any] = {},
        count: int = 1,
    ) -> "Pipeline[S]":
        assert count >= 1
        target_queue: "Queue[R]" = Pipeline.get_new_queue()
        output_pipe: "Pipeline[S]" = Pipeline()
        self.dispatcher.dispatch_to([target_queue], count)
        for _ in range(count):
            p = ClassInstancePipe(
                target_queue,
                class_constructor,
                class_method,
                output_pipe._source,
                close_method,
                class_args,
                class_kwargs,
            )
            self._register(p)
        return output_pipe

    def explode(self, explode_function: Callable[[R], Iterable[S]]) -> "Pipeline[S]":
        target_queue: "Queue[R]" = Pipeline.get_new_queue()
        output_pipe: "Pipeline[S]" = Pipeline()
        p = ExplodePipe(target_queue, explode_function, output_pipe._source)

        self._register(p)
        self.dispatcher.dispatch_to([target_queue])
        return output_pipe

    def batch(self, count: int = 2) -> "Pipeline[Iterable[R]]":
        target_queue: "Queue[R]" = Pipeline.get_new_queue()
        output_pipe: "Pipeline[Iterable[R]]" = Pipeline()
        p = BatchPipe(target_queue, output_pipe._source, count)
        self.dispatcher.dispatch_to([target_queue])

        self._register(p)
        return output_pipe

    def temporal_batch(self, time_interval: float) -> "Pipeline[Iterable[R]]":
        target_queue: "Queue[R]" = Pipeline.get_new_queue()
        output_pipe: "Pipeline[Iterable[R]]" = Pipeline()
        p = TimeBatchPipe(target_queue, output_pipe._source, time_interval)
        self.dispatcher.dispatch_to([target_queue])

        self._register(p)
        return output_pipe

    def filter(self, filter_function: Callable[[R], bool]) -> "Pipeline[R]":
        target_queue: "Queue[R]" = Pipeline.get_new_queue()
        output_pipe: "Pipeline[R]" = Pipeline()
        p = FilterPipe(target_queue, filter_function, output_pipe._source)
        self.dispatcher.dispatch_to([target_queue])

        self._register(p)
        return output_pipe

    @staticmethod
    def print_return(data: S) -> S:
        print(f"debug_{data}")
        return data

    def debug(self) -> "Pipeline[R]":
        return self.task(Pipeline.print_return)

    def kill(self) -> None:
        self.dispatcher.terminate()

    def _prepare_output_buffer(self) -> "Queue[R]":
        q: Queue[R] = Pipeline.get_new_queue()
        self.dispatcher.dispatch_to([q])
        return q

    def reduce(self, accumulator: T, reducer: Callable[[R, T], T]) -> "Pipeline[T]":
        target_queue: "Queue[R]" = Pipeline.get_new_queue()
        output_pipe: "Pipeline[T]" = Pipeline()

        p = ReducePipe(target_queue, output_pipe._source, accumulator, reducer)
        self._register(p)
        self.dispatcher.dispatch_to([target_queue])
        return output_pipe

    def wait_and_reduce(self, accumulator: T, reducer: Callable[[R, T], T]) -> "T":
        o = self.reduce(accumulator, reducer)
        [[res]] = Pipeline.wait_for_all_results([o])
        return res

    @staticmethod
    def wait_for_all_completions(
        pipes: List["Pipeline[Any]"], timeout: Optional[int] = None
    ) -> None:
        output_queues: List[Queue[Any]] = [p._prepare_output_buffer() for p in pipes]

        for o in output_queues:
            while True:
                packet = o.get(timeout=timeout)
                if GenericPipe.is_death_packet(packet):
                    break

    @staticmethod
    def wait_for_all_results(pipes: List["Pipeline[Any]"]) -> List[List[Any]]:
        output_queues: List[Optional[Queue[Any]]] = [
            p._prepare_output_buffer() for p in pipes
        ]

        outputs: List[List[Any]] = [[] for _ in pipes]

        while any(output_queues) > 0:
            for i in range(len(output_queues)):
                output_queue = output_queues[i]
                if output_queue is None:
                    continue
                try:
                    packet = output_queue.get(timeout=0.1)
                    if GenericPipe.is_death_packet(packet):
                        output_queues[i] = None
                    else:
                        outputs[i].append(packet)
                except:
                    pass

        return outputs

    def wait_for_completion(self, other_pipes: List["Pipeline[Any]"] = []) -> None:
        return Pipeline.wait_for_all_completions([self, *other_pipes])

    def wait_for_results(
        self, other_pipes: List["Pipeline[Any]"] = []
    ) -> List[List[R]]:
        return Pipeline.wait_for_all_results([self, *other_pipes])

    def wait_for_result(self) -> List[R]:
        [res] = Pipeline.wait_for_all_results([self])
        return res
