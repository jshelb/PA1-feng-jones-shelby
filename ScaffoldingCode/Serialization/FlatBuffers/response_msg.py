from typing import List
from enum import Enum
from dataclasses import dataclass

# Define the enumeration for RequestStatus
class RequestStatus(Enum):
    OK = 0
    BAD_REQUEST = 1

# Define the enumeration for ContentsStatus
class ContentsStatus(Enum):
    ORDER_PLACED = 0
    YOU_ARE_HEALTHY = 1
    BAD_REQUEST = 2

# Define the data class for Response
@dataclass
class ResponseMessage:
    seq_no: int
    ts: float
    name: str
    data: List[int]
    code: RequestStatus
    contents: ContentsStatus