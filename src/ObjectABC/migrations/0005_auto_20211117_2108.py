# Generated by Django 2.2.2 on 2021-11-17 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ObjectABC', '0004_auto_20211104_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objabcmodel',
            name='hedgedExcelFile',
        ),
        migrations.RemoveField(
            model_name='objabcmodel',
            name='outputExcelFile',
        ),
    ]
