# Generated by Django 3.1.1 on 2020-09-03 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0003_auto_20200903_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyaltyuserpoints',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
