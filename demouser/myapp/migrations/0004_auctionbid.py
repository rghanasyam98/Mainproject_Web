# Generated by Django 3.2.18 on 2023-03-29 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20230219_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auctionbid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveBigIntegerField()),
                ('auction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.auction')),
                ('cust_chitid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customerchit')),
            ],
        ),
    ]
