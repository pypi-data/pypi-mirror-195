import json
from uuid import uuid4
from typing import Type, TypeVar, ClassVar

from pydantic import ValidationError, BaseModel as PydanticBaseModel, Extra

from assimilator.core.exceptions import ParsingError


T = TypeVar("T", bound='BaseModel')


class BaseModel(PydanticBaseModel):
    id: str

    class AssimilatorConfig(PydanticBaseModel, extra=Extra.allow):
        autogenerate_id: ClassVar[bool] = True

    class Config:
        arbitrary_types_allowed = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not issubclass(cls.AssimilatorConfig, BaseModel.AssimilatorConfig):
            class InheritedConfig(cls.AssimilatorConfig, BaseModel.AssimilatorConfig):
                ...

            cls.AssimilatorConfig = InheritedConfig

        return cls

    def generate_id(self, **kwargs) -> str:
        return str(uuid4())

    def __init__(self, **kwargs):
        if self.AssimilatorConfig.autogenerate_id and kwargs.get('id') is None:
            kwargs['id'] = self.generate_id(**kwargs)

        super(BaseModel, self).__init__(**kwargs)

    @classmethod
    def loads(cls: Type['T'], data: str) -> 'T':
        try:
            return cls(**json.loads(data))
        except (ValidationError, TypeError) as exc:
            raise ParsingError(exc)


__all__ = [
    'BaseModel',
]
