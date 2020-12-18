from django.db import models
from django.conf import settings

from print_edition.models import PrintEdition


class Request(models.Model):
    print_edition = models.ForeignKey(to=PrintEdition, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    duration = models.IntegerField(choices=[(1, 1), (3, 3), (6, 6)])
    is_approved = models.BooleanField(default=False)

    @property
    def print_edition_name(self):
        return self.print_edition.name

    @property
    def price(self):
        return self.print_edition.price * self.duration

    @property
    def status(self):
        return 'Подтвержден' if self.is_approved else 'Не подтвержден'


class Subscription(models.Model):
    print_edition = models.ForeignKey(
        to=PrintEdition,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        related_query_name='subscriptions_query'
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    duration = models.IntegerField()

    @property
    def print_edition_name(self):
        return self.print_edition.name

    @property
    def address(self):
        return self.user.address

    @property
    def user_first_name(self):
        return self.user.first_name

    @property
    def user_last_name(self):
        return self.user.last_name

    @property
    def user_middle_name(self):
        return self.user.middle_name

    @property
    def user_phone(self):
        return self.user.phone
