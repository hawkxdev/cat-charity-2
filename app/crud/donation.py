"""CRUD для Donation."""

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationCreate]):
    """CRUD для пожертвований."""


donation_crud = CRUDDonation(Donation)
