# Generated by Django 3.0.8 on 2020-08-25 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0014_auto_20200821_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shopping.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Order')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='order_items', to='shopping.Item'),
        ),
    ]
