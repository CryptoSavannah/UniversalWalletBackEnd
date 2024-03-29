# Generated by Django 3.1.1 on 2021-01-13 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binusu', '0002_auto_20210112_0841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='order_amount',
            new_name='order_amount_crypto',
        ),
        migrations.AddField(
            model_name='kyc',
            name='password',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='order_amount_fiat',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
            preserve_default=False,
        ),
    ]
