# Generated by Django 2.2.9 on 2020-05-22 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posapp', '0003_userlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=150, unique=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=150, unique=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, unique=True)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('product_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.ProductBrand')),
                ('product_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.ProductCategory')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('unit_price', models.FloatField(default=0)),
                ('sales_price', models.FloatField(default=0)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.UserList')),
                ('product_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.ProductBrand')),
                ('product_cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.ProductCategory')),
                ('product_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.ProductInfo')),
            ],
        ),
    ]
