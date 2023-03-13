from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Q
from datetime import datetime,date
# import datetime
from django.db.models import F
import os
# from twilio.rest import Client

from django.conf import settings
from django.core.mail import send_mail
import smtplib

from.models import Myuser, Loan, Chit, News, Auction



# Create your views here.
def index(request):
    # print("hai")


    if request.user.is_authenticated:
        if request.user.email=="bankadmin@gmail.com":
            return redirect('admindash')
    #     if request.user.user_type == 'admin':


    return render(request, 'index.html')


def login_user(request):
    print("hai")

    email = request.POST['username']
    password = request.POST['password']
    print(email)
    print(password)
    # print(Login.objects.all())
    try:
        usr = Myuser.objects.get(email=email)
    except :
        usr = None
    print(usr)

    if(usr):
        print('email exists')
        # user = authenticate(request, email=usr.email, password=password)
        user = authenticate(username=usr.username, password=password)
        print("user",user)
        if user is not None:
            usertype = user.user_type

            if usertype == "admin":
                # return render(request, 'labadmin/admindash.html')
              login(request, user)
              return redirect('admindash')


            else:
                return HttpResponse('Staff')
        else:
            url = '/'
            resp_body = '<script>alert("Wrong password...");\
                                                            window.location="%s"</script>' % url
            return HttpResponse(resp_body)

            # return HttpResponse('Wrong password')
        # print("***")
        # print(usr.email)
        # print(usr.password)
        # if user is not None:
        #     print('success')
        # else:
        #     print('invalid user')
    else:
        url = '/'
        resp_body = '<script>alert("Invalid user...");\
                                                                    window.location="%s"</script>' % url
        return HttpResponse(resp_body)


def logoutadmin(request):
    print("hai")
    logout(request)
    # return redirect(')
    return render(request,'index.html')




@login_required
def admindash(request):
    return render(request, 'adminhome.html')

@login_required
def loan_management(request):
    print("sample table")
    loan=Loan.objects.all()
    context = {'loan': loan}
    return render(request, 'bankadmin/sample table.html', context)

@login_required
def addloan(request):
    print("add loan called")

    return render(request, 'bankadmin/add_loan.html')

@login_required
def getloanfromform(request):
    loan_name = request.POST['lname']
    rate = request.POST['rate']
    min = request.POST['min']
    max = request.POST['max']
    des = request.POST['des']
    # print(loan_name,rate,min,max,des)
    checking = Loan.objects.filter(lname=loan_name)
    if len(checking) == 0:
        loanobj = Loan()
        loanobj.lname = loan_name
        loanobj.roi = rate
        loanobj.min = min
        loanobj.max = max
        loanobj.des = des
        loanobj.save()
        url = 'loan_management'
        resp_body = '<script>alert("Loan details successfully added");\
                                                    window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    else:

        url = 'addloan'
        resp_body = '<script>alert("Already exists...");\
                                window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    # return redirect('loan_management')
    # return render(request, 'bankadmin/add_loan.html')



@login_required
def update_loan(request,lid):
    request.session['loanid']=lid
    loanobj=Loan.objects.get(id=lid)
    context={'loanobj':loanobj}
    return render(request, 'bankadmin/update_loan.html', context)

@login_required
def getupdatedloanfromform(request):
    lid = request.session['loanid']
    loan_name = request.POST['lname']
    rate = request.POST['rate']
    min = request.POST['min']
    max = request.POST['max']
    des = request.POST['des']
    loanobj=Loan.objects.get(id=lid)
    loanobj.lname=loan_name
    loanobj.des=des
    loanobj.min=min
    loanobj.max=max
    loanobj.roi=rate
    loanobj.save()
    url = 'loan_management'
    resp_body = '<script>alert("Loan details successfully updated");\
                                                        window.location="%s"</script>' % url
    return HttpResponse(resp_body)

@login_required
def delete_loan(request,lid):
    loanobj = Loan.objects.get(id=lid)
    loanobj.delete()
    return redirect('loan_management')


@login_required
def chit_management(request):
    chitobj=Chit.objects.all().order_by('-id')

    context={'chitobj':chitobj}
    return render(request,'bankadmin/chit_details.html',context)


@login_required
def addchit(request):
    return render(request,'bankadmin/addchit.html')


@login_required
def getchitfromform(request):
    chit_name = request.POST['chitname']
    duration = request.POST['period']
    tamount = request.POST['amount']
    start = request.POST['sdate']
    end = request.POST['edate']
    join_due = request.POST['ddate']
    # des = request.POST['des']
    pay_due = request.POST['paymentdue']
    print(chit_name,duration,tamount,start,end,join_due,pay_due)
    sdate_obj = datetime.strptime(start, "%m/%d/%Y")
    edate_obj = datetime.strptime(end, "%m/%d/%Y")
    ddate_obj = datetime.strptime(join_due, "%m/%d/%Y")
    print(sdate_obj.date())
    chitobj=Chit()
    chitobj.name=chit_name
    chitobj.chit_amount=tamount
    chitobj.start_date=sdate_obj.date()
    chitobj.end_date=edate_obj.date()
    chitobj.due_date=ddate_obj.date()
    chitobj.period=duration
    chitobj.pay_due_date=pay_due
    chitobj.status="Declared"
    chitobj.current_installment=0
    chitobj.save()

    url = 'chit_management'
    resp_body = '<script>alert("Chit details successfully added");\
                                                        window.location="%s"</script>' % url
    return HttpResponse(resp_body)


@login_required
def update_chit(request,cid):
    request.session['chitid'] = cid
    chitobj=Chit.objects.get(id=cid)
    sdate=chitobj.start_date
    edate=chitobj.end_date
    ddate=chitobj.due_date
    print(sdate)
    # sdate=str(sdate)
    new_date_start = sdate.strftime('%m/%d/%Y')
    print('sdate',new_date_start)
    new_date_end = edate.strftime('%m/%d/%Y')
    print('edate', new_date_end)
    new_date_due = ddate.strftime('%m/%d/%Y')
    print('ddate', new_date_due)
    # 'new_date_start': new_date_start, 'new_date_end': new_date_end, 'new_date_due': new_date_due
    context={'x':chitobj,'new_date_start': new_date_start, 'new_date_end': new_date_end, 'new_date_due': new_date_due}
    return render(request,'bankadmin/update_chit.html',context)




@login_required
def getupdatedchitfromform(request):
    cid=request.session['chitid']
    chit_name = request.POST['chitname']
    duration = request.POST['period']
    tamount = request.POST['amount']
    start = request.POST['sdate']
    end = request.POST['edate']
    join_due = request.POST['ddate']
    # des = request.POST['des']
    pay_due = request.POST['paymentdue']
    print(chit_name, duration, tamount, start, end, join_due, pay_due)
    sdate_obj = datetime.strptime(start, "%m/%d/%Y")
    edate_obj = datetime.strptime(end, "%m/%d/%Y")
    ddate_obj = datetime.strptime(join_due, "%m/%d/%Y")
    print(sdate_obj.date())
    chitobj = Chit.objects.get(id=cid)
    chitobj.name = chit_name
    chitobj.chit_amount = tamount
    chitobj.start_date = sdate_obj.date()
    chitobj.end_date = edate_obj.date()
    chitobj.due_date = ddate_obj.date()
    chitobj.period = duration
    chitobj.pay_due_date = pay_due
    # chitobj.status = "Declared"
    # chitobj.current_installment = 0
    chitobj.save()


    url = 'chit_management'
    resp_body = '<script>alert("Chit details successfully updated");\
                                                            window.location="%s"</script>' % url
    return HttpResponse(resp_body)


@login_required
def delete_chit(request,cid):
    chitobj = Chit.objects.get(id=cid)
    chitobj.delete()
    return redirect('chit_management')


@login_required
def news_management(request):
    print("search")

    news = News.objects.all().order_by('-id')
    if request.method == "POST":
        print("search")
        title = request.POST['search']
        news=News.objects.filter(title__contains=title)
    context = {'news': news}

    return render(request,'bankadmin/news_management.html',context)


@login_required
def addnews(request):
    return render(request, 'bankadmin/add_news.html')



@login_required
def getnewsfromform(request):
    title = request.POST['title']
    des = request.POST['des']
    type = request.POST['type']
    image = request.FILES['file-upload']
    print(title,des,type,image)
    newsobj=News()
    newsobj.title=title
    newsobj.content=des
    newsobj.type=type
    newsobj.image=image
    newsobj.save()
    url = 'news_management'
    resp_body = '<script>alert("News details successfully added");\
                                                               window.location="%s"</script>' % url
    return HttpResponse(resp_body)

@login_required
def delete_news(request,nid):
    newsobj=News.objects.get(id=nid)
    newsobj.delete()
    return redirect('news_management')

@login_required
def update_news(request,nid):
    request.session['newsid'] = nid
    newsobj = News.objects.get(id=nid)
    context={'newsobj':newsobj}
    return render(request, 'bankadmin/update_news.html',context)

@login_required
def getupdatednewsfromform(request):
    print("news update")
    nid = request.session['newsid']
    title = request.POST['title']
    des = request.POST['des']
    type = request.POST['type']
    if 'file-upload' in request.FILES:
        # File was uploaded
        image = request.FILES['file-upload']
    else:
        # No file was uploaded
        image = None

    print(title, des, type, image)
    newsobj = News.objects.get(id=nid)
    newsobj.title = title
    newsobj.content = des
    newsobj.type = type
    if image is not None:
        newsobj.image = image

    newsobj.save()

    url = 'news_management'
    resp_body = '<script>alert("News details successfully Updated");\
                                                                  window.location="%s"</script>' % url
    return HttpResponse(resp_body)


@login_required
def auction_management(request):
    auction=Auction.objects.all().order_by('-id')
    context={'auction':auction}
    return render(request, 'bankadmin/auction_management.html',context)


@login_required
def addauction(request):
    chit=Chit.objects.filter(status="ongoing")
    context={'chit':chit}
    return render(request, 'bankadmin/add_auction.html',context)


@login_required
def getauctionfromform(request):
    chit_id = request.POST['chitno']
    auction_date = request.POST['adate']
    auction_time = request.POST['atime']
    print(chit_id,auction_date,auction_time)

    input_time = datetime.strptime(auction_time, '%I:%M %p')
    print( input_time.strftime('%H:%M'))
    output_time=input_time.strftime('%H:%M')
    # formatted_time = output_time.strftime('%I:%M %p')
    # print(formatted_time)

    date_obj = datetime.strptime(auction_date, "%m/%d/%Y")
    # chitobj.start_date=sdate_obj.date()

    auction=Auction()
    auction.chitid_id=chit_id
    auction.auction_date=date_obj.date()
    # auction.auction_time=auction_time
    auction.auction_time=output_time

    auction.save()
    url = 'auction_management'
    resp_body = '<script>alert("Auction details successfully Added");\
                                                                      window.location="%s"</script>' % url
    return HttpResponse(resp_body)


@login_required
def delete_auction(request,aid):
    auction=Auction.objects.get(id=aid)
    auction.delete()
    return redirect('auction_management')

@login_required
def update_auction(request,aid):
    request.session['auction_id']=aid
    auction=Auction.objects.get(id=aid)
    # print(auction.auction_time)
    # formatted_time = auction.auction_time.strftime('%I:%M %p')
    # print(formatted_time)
    new_date = auction.auction_date.strftime('%m/%d/%Y')
    chit=Chit.objects.filter(status="ongoing")
    context={'auction':auction,'chit':chit,'new_date':new_date}
    return render(request,'bankadmin/update_auction.html',context)

@login_required
def getupdatedauctionfromform(request):
    aid=request.session['auction_id']
    chit_id = request.POST['chitno']
    auction_date = request.POST['adate']
    auction_time = request.POST['atime']
    print(chit_id, auction_date, auction_time)
    date_obj = datetime.strptime(auction_date, "%m/%d/%Y")

    input_time = datetime.strptime(auction_time, '%I:%M %p')
    print(input_time.strftime('%H:%M'))
    output_time = input_time.strftime('%H:%M')

    auction = Auction.objects.get(id=aid)
    auction.chitid_id = chit_id
    auction.auction_date = date_obj.date()
    auction.auction_time = output_time
    auction.save()
    url = 'auction_management'
    resp_body = '<script>alert("Auction details successfully Updated");\
                                                                         window.location="%s"</script>' % url
    return HttpResponse(resp_body)
