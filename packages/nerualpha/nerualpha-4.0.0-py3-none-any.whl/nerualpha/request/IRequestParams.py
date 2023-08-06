from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod

from nerualpha.services.config.IUrlObject import IUrlObject
from nerualpha.request.responseTypes import ResponseTypes

T = TypeVar("T")


#interface
class IRequestParams(ABC,Generic[T]):
    method:str
    url:IUrlObject
    data:T
    headers:Dict[str,str]
    responseType:ResponseTypes
