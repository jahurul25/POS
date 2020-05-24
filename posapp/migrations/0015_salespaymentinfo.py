# Generated by Django 2.2.9 on 2020-05-24 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posapp', '0014_invoicewisediscount'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesPaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_invo', models.IntegerField(default=0)),
                ('total_amount', models.IntegerField(default=0)),
                ('cash_amount', models.IntegerField(default=0)),
                ('gift_card_amount', models.IntegerField(default=0)),
                ('card_number', models.IntegerField(default=0)),
                ('payment_method', models.CharField(max_length=50)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('confirm_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posapp.UserList')),
            ],
        ),
    ]