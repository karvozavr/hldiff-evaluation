from abc import ABC, abstractmethod
from typing import Iterable


class StepData(ABC):

    @abstractmethod
    def serialize(self) -> str:
        pass

    @abstractmethod
    def should_persist(self) -> bool:
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self, data):
        pass


class Pipeline:

    def __init__(self, last_step):
        self.step = last_step

    @staticmethod
    def for_dataset(data: Iterable):
        pass


class ProcessingStep(ABC):

    def __init__(self):
        self._parent = None

    @abstractmethod
    def process(self, data: StepData) -> StepData:
        pass

    def set_parent(self, parent):
        pass

    def then(self, next_step):
        next_step.set_parent(self)
        return next_step

    def build(self) -> Pipeline:
        return Pipeline(self)


class _InitialStep(ProcessingStep):

    def process(self, data: StepData) -> StepData:
        return data
