from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.

class ChoiceParams(models.Model):
    client = 'client'
    kitchen = 'kitchen'
    check_types = [
        (client, 'client'),
        (kitchen, 'kitchen')
    ]
    new = 'new'
    rendered = 'rendered'
    printed = 'printed'
    status = [
        (new, 'new'),
        (rendered, 'rendered'),
        (printed, 'printed')
    ]

    class Meta:
        abstract = True


class Printer(ChoiceParams):
    name = models.CharField(max_length=200, verbose_name='Название принтера')
    api_key = models.CharField(max_length=2500, unique=True, blank=False, null=False, verbose_name='Ключ доступа к API')
    check_type = models.CharField(max_length=7, choices=ChoiceParams.check_types, verbose_name='Тип чека')
    point_id = models.IntegerField(verbose_name='точка привязки принтера')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтеры'


class Check(ChoiceParams):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, verbose_name='Принтер', related_name='checks_set')
    check_type = models.CharField(max_length=7, choices=ChoiceParams.check_types, verbose_name='Тип чека')
    order = JSONField(verbose_name='Информация о заказе')
    status = models.CharField(max_length=8, choices=ChoiceParams.status, default=ChoiceParams.new, verbose_name='Статус чека')
    pdf_file = models.FileField(upload_to='pdf/', null=True, blank=True, verbose_name='PDF-файл')

    def __str__(self):
        return f'{self.order["id"]}_{self.check_type}'

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
