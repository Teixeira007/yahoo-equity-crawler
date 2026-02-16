from dataclasses import dataclass
from typing import Optional

@dataclass
class Equity:
    symbol: Optional[str]
    name: Optional[str]
    price: Optional[float]