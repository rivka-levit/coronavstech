from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    class CompanyStatus(models.TextChoices):
        LAYOFFS = 'Layoffs'
        HIRING_FREEZE = 'Hiring Freeze'
        HIRING = 'Hiring'

    name = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=30,
                              choices=CompanyStatus.choices,
                              default=CompanyStatus.HIRING)
    last_updated = models.DateTimeField(default=now, editable=True)
    app_link = models.URLField(blank=True)
    notes = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.name}'
