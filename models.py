from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from datetime import datetime

class Commodity(str, Enum):
    ELECTRICITY = "Electricity"
    HYDROGEN = "Hydrogen"
    HEAT = "Heat"
    GAS = "Gas"

class TimeFrame(str, Enum):
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    YEAR = "1y"

class TradeType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class TradeStatus(str, Enum):
    COMPLETED = "Completed"
    PENDING = "Pending"

class ResourceStatus(str, Enum):
    SURPLUS = "surplus"
    DEFICIT = "deficit"

class Amount(BaseModel):
    value: float
    measurement_unit: str

class Price(BaseModel):
    value: float
    currency: str

class Trade(BaseModel):
    id: str
    commodity: Commodity
    type: TradeType
    amount: Amount
    price: Price
    status: TradeStatus
    time: Optional[datetime] = None
    requester_company: str
    fulfiller_company: Optional[str] = None

class ResourceState(BaseModel):
    commodity: Commodity
    status: ResourceStatus
    amount: Amount

class Company(BaseModel):
    name: str
    location: str
    statuses: List[ResourceState]
    last_active: datetime

class PricePoint(BaseModel):
    timestamp: datetime
    price: float

class SavingsResult(BaseModel):
    total_savings: float
    savings_by_commodity: dict[Commodity, float]
    currency: str
    timeframe: TimeFrame