# Generated by Django 4.2.3 on 2023-08-06 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SecondChanceEmporiumApp', '0007_productinorder_alter_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 14, 11, 43, 40544)),
        ),
    ]
