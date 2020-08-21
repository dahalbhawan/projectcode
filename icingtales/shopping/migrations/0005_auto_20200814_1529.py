# Generated by Django 3.0.8 on 2020-08-14 05:29

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0004_auto_20200814_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(help_text='Required format YYYY-MM-DD (e.g, 1990-10-25)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Example: +61451234567', max_length=128, region=None, unique=True),
        ),
    ]