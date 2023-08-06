from typing import Union

import pydantic


class Expression(pydantic.BaseModel):
    expr: Union[float, int, str]
