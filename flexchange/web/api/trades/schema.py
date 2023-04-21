from datetime import date, datetime

from pydantic import BaseModel, Field


class TradeModelDTO(BaseModel):
    """
    DTO for trade models.

    It returned when accessing trade models from the API.
    """

    id: str = Field(
        None,
        description="Unique id of the trade as defined by the exchange",
        example="trade_123",
    )
    price: int = Field(None, description="Price in eurocent/MWh.", example=200)
    quantity: int = Field(None, description="Quantity in MW.", example=12)
    direction: str = Field(
        None,
        description="Direction of the trade from the perspective of flew-power, can be either buy or sell.",
        regex=r"^(buy|sell)$",
    )
    delivery_day: date = Field(
        None,
        description="Day on which the energy has to be delivered in local time.",
    )
    delivery_hour: int = Field(
        None,
        description="Hour during which the energy has to be delivered in local time.",
        example=14,
    )
    trader_id: str = Field(
        None,
        description="Unique id of a trader (bot or team member).",
        example="MirkoT",
    )
    execution_time: datetime = Field(
        None,
        description="UTC datetime at which the trade occured on the exchange.",
    )

    class Config:
        orm_mode = True
