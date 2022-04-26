# Generated by Django 3.1.1 on 2022-04-26 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binusu', '0022_auto_20220426_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('UNFULFILLED', 'UNFULFILLED'), ('FULFILLED', 'FULFILLED'), ('PENDING', 'PENDING'), ('FAILED', 'FAILED'), ('DECLINED', 'DECLINED'), ('PROCESSING', 'PROCESSING')], default='UNFULFILLED', max_length=15),
        ),
    ]
