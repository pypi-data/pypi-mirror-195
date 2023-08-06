from multiprocessing import Queue
from typing import Iterable, List, Optional, TypeVar
from .generic import GenericPipe

R = TypeVar("R")


class BatchPipe(GenericPipe[R, Iterable[R]]):
    def __init__(
        self, source: "Queue[R]", target: "Queue[Iterable[R]]", batch_size: int
    ):
        super().__init__(source, target)
        self._batch_size = batch_size
        self._datas: List[R] = []

    def perform_task(self, data: R) -> Optional[Iterable[R]]:  # type: ignore
        self._datas.append(data)
        if len(self._datas) >= self._batch_size:
            packet, self._datas = (
                self._datas[: self._batch_size],
                self._datas[self._batch_size :],
            )
            return packet

    def dispatch_to_next(self, processed: Optional[Iterable[R]]) -> None:
        if processed is None:
            return
        super().dispatch_to_next(processed)
