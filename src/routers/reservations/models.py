from datetime import datetime

from pydantic import BaseModel


class ReservationPaymentModel(BaseModel):
    card_number: str
    cvv: str
    expiration_date: datetime
