# Generated by Django 3.1.1 on 2021-01-27 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binusu', '0006_auto_20210127_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordresets',
            name='reset_used',
            field=models.BooleanField(default=False),
        ),
    ]