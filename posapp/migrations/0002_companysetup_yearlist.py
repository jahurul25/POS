# Generated by Django 2.2.9 on 2020-05-20 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=0)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanySetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200, unique=True)),
                ('company_mobile', models.CharField(max_length=15)),
                ('company_email', models.CharField(max_length=15)),
                ('company_address', models.CharField(max_length=10)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('country_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.CountryList')),
                ('starting_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.YearList')),
            ],
        ),
    ]
