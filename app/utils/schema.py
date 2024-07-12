from typing import Union, get_args, get_origin, get_type_hints

from fastapi import Form
from pydantic import BaseModel

PydanticSchemaType = type[BaseModel]


class FormConvertSchema(BaseModel):
    """pydantic 클래스의 정의된 필드를 formdata필드로 전환해주는 base class"""

    @classmethod
    def as_form(cls: PydanticSchemaType) -> PydanticSchemaType:
        new_params = {}

        # Optional 타입 처리

        for field_name, model_fields in cls.model_fields.items():
            print(get_type_hints(model_fields))
            annotation = model_fields.annotation
            if get_origin(annotation) is Union and type(None) in get_args(annotation):
                annotation = get_args(annotation)[0]

            new_params[field_name] = (
                annotation,
                Form(
                    default=model_fields.default,
                    title=model_fields.title,
                ),
            )
        return type("FormModel", (cls,), {"__annotations__": new_params})
