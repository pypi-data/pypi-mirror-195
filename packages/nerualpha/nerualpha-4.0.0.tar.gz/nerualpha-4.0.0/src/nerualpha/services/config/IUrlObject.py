from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod



#interface
class IUrlObject(ABC):
    host:str
    query:Dict[str,str]
    pathname:str
