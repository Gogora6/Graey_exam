from django.db.models import IntegerChoices


class TicketStatus(IntegerChoices):
    unavailable = 0
    available = 1
