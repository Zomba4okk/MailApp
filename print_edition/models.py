from datetime import datetime

from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=20)


class PrintEdition(models.Model):
    name = models.CharField(max_length=20)
    type = models.ForeignKey(to=Type, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.name

    def get_report_data(self, start_date, end_date):
        return self.subscriptions.filter(
            start_date__gte=datetime.strptime(start_date, '%Y-%m-%d'),
            start_date__lte=datetime.strptime(end_date, '%Y-%m-%d'),
        ).values(
            'print_edition__name',
            'start_date',
            'duration',
            'print_edition__price',
            'user__address',
            'user__last_name',
            'user__first_name',
            'user__middle_name',
        ).all()
