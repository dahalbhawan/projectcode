# Generated by Django 3.0.8 on 2020-08-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0021_auto_20200828_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orders',
            field=models.ManyToManyField(through='shopping.ItemOrder', to='shopping.Item'),
        ),
    ]
