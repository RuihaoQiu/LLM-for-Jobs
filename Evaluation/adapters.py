from typing import Any

class ModelAdapter:
    name = "base"
    def predict(self, record: dict) -> Any:
        """Given a record {task, input}, return prediction"""
        raise NotImplementedError

class EchoAdapter(ModelAdapter):
    """Dummy baseline: just echo gold"""
    name = "echo"
    def predict(self, record: dict) -> Any:
        return record["gold"]
