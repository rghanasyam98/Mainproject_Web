from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Myuser(AbstractUser):
    user_type = models.CharField(max_length=20, null=True)
    phone = models.BigIntegerField(default=9995936507)



class News(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=60)
    image = models.ImageField(upload_to='images/', null=True)
    # date = models.DateField()
    type = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Loan(models.Model):
    lname=models.CharField(max_length=30)
    des= models.CharField(max_length=150)
    roi= models.FloatField(default=0.0)
    min=models.PositiveBigIntegerField(default=0)
    max=models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Accountrequest(models.Model):
    uid = models.ForeignKey(Myuser, on_delete=models.CASCADE)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    dob = models.DateField()
    address=models.CharField(max_length=60)
    marital_status = models.CharField(max_length=15)
    namefms=models.CharField(max_length=25)
    dependants=models.PositiveIntegerField(default=0)
    nationality = models.CharField(max_length=25)
    occupation = models.CharField(max_length=25)
    income = models.CharField(max_length=20)
    qualification = models.CharField(max_length=15)
    type = models.CharField(max_length=15, null=True)
    pan = models.CharField(max_length=20)
    aadhar = models.CharField(max_length=20)
    nomname = models.CharField(max_length=25)
    nomaddress = models.CharField(max_length=60)
    relation = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/')
    status = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Account(models.Model):
    # id =models.AutoField(primary_key=True, verbose_name='ID',
    #                       serialize=False, auto_created=True,
    #                       db_column='id', help_text='My custom help text',
    #                       start=123456)
    accrid= models.ForeignKey(Accountrequest, on_delete=models.CASCADE)
    balance=models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Kyc(models.Model):
    account_number=models.ForeignKey(Account, on_delete=models.CASCADE)
    form = models.FileField(upload_to='docs/', null=True, max_length=255)
    proof = models.FileField(upload_to='docs/', null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customerloan(models.Model):
    loanid=models.ForeignKey(Loan, on_delete=models.CASCADE)
    account_number=models.ForeignKey(Account, on_delete=models.CASCADE)
    loan_amount=models.PositiveBigIntegerField()
    min_date=models.DateField(null=True)
    max_date=models.DateField(null=True)
    emi=models.PositiveIntegerField(null=True)
    status = models.CharField(max_length=15,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Chit(models.Model):
    # id=models.AutoField(primary_key=True, verbose_name='ID',
    #                       serialize=False, auto_created=True,
    #                       db_column='id', help_text='My custom help text',
    #                       start=23456)
    name = models.CharField(max_length=20)
    chit_amount=models.PositiveBigIntegerField()
    period=models.PositiveIntegerField()
    due_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    pay_due_date = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    current_installment = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customerchit(models.Model):
    chitid=models.ForeignKey(Chit, on_delete=models.CASCADE)
    account_number=models.ForeignKey(Account, on_delete=models.CASCADE)
    current_payment_count = models.PositiveIntegerField()
    chittal_number = models.PositiveIntegerField()
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Auction(models.Model):
    chitid = models.ForeignKey(Chit, on_delete=models.CASCADE)
    auction_date = models.DateField()
    auction_time=models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Result(models.Model):
    auction_id= models.ForeignKey(Auction, on_delete=models.CASCADE)
    cust_chitid= models.ForeignKey(Customerchit, on_delete=models.CASCADE)
    won_amount = models.PositiveBigIntegerField()
    security = models.FileField(upload_to='docs/', null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    cust_chitid= models.ForeignKey(Customerchit, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    transactionid = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    chitid=  models.ForeignKey(Chit, on_delete=models.CASCADE)
    content = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Auctionbid(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    cust_chitid = models.ForeignKey(Customerchit, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()

class Auctionbidamount(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    cust_chitid = models.ForeignKey(Customerchit, on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=12, decimal_places=4)

class Auctionbidamountlatest(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    cust_chitid = models.ForeignKey(Customerchit, on_delete=models.CASCADE)
    amount =  models.DecimalField(max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Installment(models.Model):
    cust_chitid = models.ForeignKey(Customerchit, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
