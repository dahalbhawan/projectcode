# Generated by Django 3.0.8 on 2020-08-20 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0008_auto_20200820_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='image',
            field=models.ImageField(blank=True, upload_to='static'),
        ),
    ]