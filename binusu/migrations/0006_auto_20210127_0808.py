# Generated by Django 3.1.1 on 2021-01-27 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('binusu', '0005_auto_20210113_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='activated_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='kyc',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PasswordResets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reset_token', models.CharField(max_length=250)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('related_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_related_account', to='binusu.kyc')),
            ],
        ),
    ]