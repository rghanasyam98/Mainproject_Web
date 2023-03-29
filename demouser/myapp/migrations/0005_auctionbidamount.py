# Generated by Django 3.2.18 on 2023-03-29 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auctionbid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auctionbidamount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=12)),
                ('auction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.auction')),
                ('cust_chitid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customerchit')),
            ],
        ),
    ]