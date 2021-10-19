# Generated by Django 3.2.8 on 2021-10-19 13:12

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
            name='LoanTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('duration_years', models.PositiveIntegerField()),
                ('intrest_rate', models.FloatField()),
                ('max_amount', models.PositiveIntegerField()),
                ('min_amount', models.PositiveIntegerField()),
                ('creator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TermApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('IP', 'In Process'), ('AP', 'Approved'), ('DN', 'Denied')], default='IP', max_length=2)),
                ('amount', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('term_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.loanterm')),
            ],
        ),
        migrations.CreateModel(
            name='LoanFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('duration_years', models.PositiveIntegerField()),
                ('intrest_rate', models.FloatField()),
                ('max_amount', models.PositiveIntegerField()),
                ('min_amount', models.PositiveIntegerField()),
                ('creator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FundApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('IP', 'In Process'), ('AP', 'Approved'), ('DN', 'Denied')], default='IP', max_length=2)),
                ('amount', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('fund_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.loanfund')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
