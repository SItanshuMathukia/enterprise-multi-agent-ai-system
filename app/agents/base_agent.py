from abc import ABC, abstractmethod
from app.core.logging import logger
from app.core.llm import llm


class BaseAgent(ABC):

    @abstractmethod
    def execute(self, task: str):
        pass


logger.info("Base agent started")