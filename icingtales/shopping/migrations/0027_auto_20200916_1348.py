# Generated by Django 3.1.1 on 2020-09-16 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0026_auto_20200911_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flavor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surcharge', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='available_flavors',
            field=models.ManyToManyField(to='shopping.Flavor'),
        ),
    ]
