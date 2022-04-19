from datetime import datetime

from django.db import models


class RecentlyPostManager(models.Manager):
    def get_query_set(self):
        today = datetime.today()
        start_date = datetime(today.year, today.month, today.day)
        end_date = datetime(today.year, today.month, today.day + 7)
        return self.filter(created__gte=start_date, created__lte=end_date)
# super().get_queryset().annotate(number_of_task=Count('task')).filter(number_of_task=0)

