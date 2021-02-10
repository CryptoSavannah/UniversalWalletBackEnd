# Generated by Django 3.1.1 on 2021-02-09 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('binusu', '0009_auto_20210202_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('email_address', models.CharField(max_length=250)),
                ('password', models.CharField(blank=True, max_length=250, null=True)),
                ('role', models.IntegerField()),
                ('active', models.BooleanField(default=False)),
                ('account_status', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='kyc',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='orders',
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='UserRefreshOtp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refresh_otp', models.CharField(max_length=5)),
                ('token_status', models.BooleanField(default=True)),
                ('token_expiry', models.DateTimeField(blank=True, null=True)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('related_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_refresh_otps', to='binusu.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserLogins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('last_token', models.CharField(blank=True, max_length=250, null=True)),
                ('related_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_logins', to='binusu.user')),
            ],
        ),
    ]