# Generated by Django 3.1.1 on 2020-09-16 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0027_auto_20200916_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='flavor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flavor_items', to='shopping.flavor'),
        ),
    ]
