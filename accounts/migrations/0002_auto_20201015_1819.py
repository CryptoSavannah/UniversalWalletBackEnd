# Generated by Django 3.1.1 on 2020-10-15 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pin_code',
        ),
        migrations.AddField(
            model_name='user',
            name='prefix',
            field=models.CharField(blank=True, choices=[('+256', '+256'), ('+254', '+254')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
