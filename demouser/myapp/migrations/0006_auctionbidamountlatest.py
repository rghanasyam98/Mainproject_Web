# Generated by Django 3.2.18 on 2023-03-30 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auctionbidamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auctionbidamountlatest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=4, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.auction')),
                ('cust_chitid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customerchit')),
            ],
        ),
    ]
