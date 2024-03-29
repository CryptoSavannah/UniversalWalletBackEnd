# Generated by Django 3.1.1 on 2020-09-03 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoyaltyProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name', models.CharField(max_length=250)),
                ('products_attached', models.CharField(max_length=250)),
                ('program_percentage', models.DecimalField(decimal_places=2, max_digits=20)),
                ('partner_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('status', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partnerships',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_name', models.CharField(max_length=250)),
                ('partner_product', models.CharField(max_length=250)),
                ('partner_contact', models.CharField(max_length=250)),
                ('percentage_points', models.DecimalField(decimal_places=2, max_digits=20)),
                ('partner_returns', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('status', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoyaltyUserPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_accrued', models.DecimalField(decimal_places=2, max_digits=20)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=20)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('related_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_related', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoyaltyProgramTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receipt_number', models.CharField(max_length=250)),
                ('points_awarded', models.DecimalField(decimal_places=2, max_digits=20)),
                ('payment_mode', models.CharField(default='CASH', max_length=250)),
                ('transaction_date', models.DateTimeField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('related_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_related', to='loyalty.loyaltyprogram')),
            ],
        ),
        migrations.AddField(
            model_name='loyaltyprogram',
            name='program_partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='program_partner', to='loyalty.partnerships'),
        ),
    ]
