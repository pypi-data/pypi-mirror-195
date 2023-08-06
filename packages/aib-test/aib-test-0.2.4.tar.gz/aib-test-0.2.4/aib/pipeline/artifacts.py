# from torch.nn.modules import Module as PTModel
# from xgboost import XGBModel
# from tensorflow.python.keras.models import Model as TFModel
from typing import Annotated, TypeVar, Any
from pydantic import BaseModel, Extra, validator
from .exceptions import *


class ModelAnnotation:
    """Input type marker"""


T = TypeVar('T')
Model = Annotated[T, ModelAnnotation]
Model.__doc__ = """Type generic used to represent an input artifact of type ``T``, where ``T`` is an artifact class."""


class Artifact(BaseModel):
    TYPE_NAME = "Base"
    name: str
    metadata: dict | None = None

    class Config:
        extra = Extra.forbid


class TF(Artifact):
    TYPE_NAME = "Model"
    type = "TF"
    model: object

    @validator("model")
    @classmethod  # Optional, but your linter may like it.
    def check_model_type(cls, value):
        from tensorflow.python.keras.models import Model as FTModel
        for base in value.__class__.__bases__:
            if base == FTModel().__class__:
                return value
        else:
            raise TypeNotMatched(str(value.__class__.__bases__))


class XGBoost(Artifact):
    TYPE_NAME = "Model"
    type = "XGBoost"
    model: object

    @validator("model")
    @classmethod
    def check_model_type(cls, value):
        from xgboost import XGBModel
        for base in value.__class__.__bases__:
            if base == XGBModel().__class__:
                return value
        else:
            raise TypeNotMatched(str(value.__class__.__bases__))


class Pytorch(Artifact):
    TYPE_NAME = "Model"
    type = "Pytorch"
    model: object

    @validator("model")
    @classmethod
    def check_model_type(cls, value):
        from torch.nn.modules import Module as PTModel
        for base in value.__class__.__bases__:
            if base == PTModel().__class__:
                return value
        else:
            raise TypeNotMatched(str(value.__class__.__bases__))


class ModelType(object):
    TF = "TF"
    Pytorch = "Pytorch"
    XGBoost = "XGBoost"


