from pydantic import BaseModel, Field
from typing import Optional

class SolorSystemInvoiceForm(BaseModel):
    client_name : str = Field(
        description = "Client Name"
    )
    cnic_number : str = Field(
        description = "Client CNIC Number"
    )
    address : str = Field(
        description = "Client Address"
    )
    total_panels : int = Field(
        description = "Number of Panels"
    )
    per_panel_price : float = Field(
        description = "Per Panel Price"
    )
    total_amount : float = Field(
        description = "Total Amount"
    )
    discount : Optional[float] = Field(
        default = 0.0,
        description = "Discount"
    )
    receive_payment : float = Field(
        description = "Amount Received"
    )
    remaining_amount : float = Field(
        description = "Remaining Amount"
    )
