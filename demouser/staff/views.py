from django.shortcuts import render
from calendar import monthrange

from django.shortcuts import render
from twilio.rest import Client

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
import json
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from myapp.models import Myuser, Accountrequest, Account, News, Loan, Customerloan, Kyc, Chit, Customerchit, Auction, \
    Auctionbid, Auctionbidamount, Auctionbidamountlatest, Result, Installment, Payment


def view_accountrequests(request):
    accountrequest=Accountrequest.objects.filter(status="pending").order_by("-id")
    popupstatus = False
    context={'accountrequest':accountrequest,'popupstatus': popupstatus,}
    return render(request, 'bankstaff/accountrequest.html',context)

@csrf_exempt
def accept_accountrequest(request,reqid):
    if request.method == 'POST':
        print("entered accept")
        # Retrieve the ID from the request data
        # id = request.POST.get('id')
        print(reqid)
        accreq = get_object_or_404(Accountrequest, id=reqid)

        # Update the status to "added"
        accreq.status = "added"
        accreq.save()
        acc=Account()
        acc.accrid_id=reqid
        acc.balance=0
        acc.save()
        accountrequests = Accountrequest.objects.filter(status="pending").order_by("-id")
        serialized_accountrequests = serializers.serialize('json', accountrequests)
        # Process the request and return a JSON response
        # ...
        # Example response:
        # return JsonResponse({'message': 'Details accepted successfully!', 'accountrequests': serialized_accountrequests})
        return JsonResponse({'message': 'Details accepted successfully!'})

    else:
        # Handle other HTTP methods (e.g. GET)
        # ...
        pass


@csrf_exempt
def reject_accountrequest(request, reqid):
    if request.method == 'POST':
        print("entered reject")
        # Retrieve the ID from the request data
        # id = request.POST.get('id')
        print(reqid)
        accreq = get_object_or_404(Accountrequest, id=reqid)

        # Update the status to "added"
        accreq.status = "rejected"
        accreq.save()


        # Process the request and return a JSON response
        # ...
        # Example response:
        return JsonResponse({'message': 'Rejected successfully!'})
    else:
        # Handle other HTTP methods (e.g. GET)
        # ...
        pass

def view_loanrequests(request):
    loanrequest = Customerloan.objects.filter(Q(status="pending") | Q(status="eligible")).order_by("-id")
    popupstatus = False
    loanobj=Loan.objects.all()
    approvedloanrequests=Customerloan.objects.filter(status="approved").order_by("-id")
    context = {'loanrequest': loanrequest, 'popupstatus': popupstatus,'loanobj':loanobj,'approvedloanrequests':approvedloanrequests }
    return render(request, 'bankstaff/loanrequest.html', context)

def viewmoredetailsofloanrequest(request,reqid):
    obj=Customerloan.objects.get(id=reqid)
    print(obj.id)
    context = {'loanrequest': obj,}
    return render(request, 'bankstaff/viewmoreloanrequestdetails.html',context )


def viewmoredetailsofloanrequest2(request,reqid):
    obj=Customerloan.objects.get(id=reqid)
    print(obj.id)
    context = {'loanrequest': obj,}
    return render(request, 'bankstaff/viewmoreloanrequestdetails2.html',context )

def reject_loanrequest(request,reqid):
    obj = Customerloan.objects.get(id=reqid)
    obj.status="rejected"
    obj.save()
    phone=obj.account_number.accrid.uid.phone
    print("phone",phone)
    mob = '+91' +str(phone)
    # smsmsg ="Your request for "+str(obj.loanid.lname)+"is rejected. Contact bank for more details..."
    smsmsg = "Your request for loan is rejected.."
    account_sid = 'AC8bb9a55c8e2e83a3aec7a1af351d600b'
    auth_token = '6543e661182f0c1f5fccf34e70449896'
    client = Client(account_sid, auth_token)
    mob = '+91' + str(phone)
    smsmsg = "Your OTP for verification is : "
    account_sid = 'AC8bb9a55c8e2e83a3aec7a1af351d600b'
    auth_token = '5974a20ad0f76d34c634ed0bdd3561b0'
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(

            body=smsmsg,
            from_='+16829002201',
            to=mob

        )
        url = '/staff/view_loanrequests'
        resp_body = '<script>alert("Successfully rejected..");\
                                                                                             window.location="%s"</script>' % url
        return HttpResponse(resp_body)
    except:
        url = '/staff/view_loanrequests'
        resp_body = '<script>alert("Failed to reject. Please try after some time..");\
                                                                                     window.location="%s"</script>' % url
        return HttpResponse(resp_body)


#
# def listloan(request):
#     print("entered")
#     cat_id = request.GET['cat_id']
#     print(cat_id)
#     cat = Customerloan.objects.filter(loanid_id=cat_id)
#     loan_list_size = len(cat)
#     loan_list = [None] * loan_list_size
#     for i, x in enumerate(cat):
#         loan_dict = {
#             'fname': x.account_number.accrid.fname,
#             'lname': x.account_number.accrid.lname,
#             'account': x.account_number_id,
#             'loan': x.loanid.lname,
#             'amount': x.loan_amount,
#             'date': x.created_at.date(),
#             'status': x.status,
#         }
#         loan_list[i] = loan_dict
#     serialized_data = loan_list
#     print(serialized_data)
#     return JsonResponse( serialized_data)

from django.http import JsonResponse

def listloan(request):
    print("entered")
    cat_id = request.GET['cat_id']
    print(cat_id)
    cat = Customerloan.objects.filter(loanid_id=cat_id)
    loan_list_size = len(cat)
    loan_list = [None] * loan_list_size
    for i, x in enumerate(cat):
        loan_dict = {
            'id':x.id,
            'fname': x.account_number.accrid.fname,
            'lname': x.account_number.accrid.lname,
            'account': x.account_number_id,
            'loan': x.loanid.lname,
            'amount': x.loan_amount,
            'date': x.created_at.date(),
            'status': x.status,
        }
        loan_list[i] = loan_dict
    serialized_data = loan_list
    print(serialized_data)
    return JsonResponse({'data': serialized_data}, safe=False)


import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def approve_loan(request, reqid):
    if request.method == "POST":
        data = json.loads(request.body)
        startdate = data.get("startdate")
        enddate = data.get("enddate")
        emi = data.get("emi")
        # print(startdate,enddate,emi,reqid)
        obj=Customerloan.objects.get(id=reqid)
        obj.emi=emi
        obj.min_date=startdate
        obj.max_date=enddate
        obj.save()
        # Do something with the data here, e.g. save it to the database

        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})

#
# def view_sample(request):
#     chitobj=Chit.objects.filter(due_date__gte=date.today())
#     chitobj2 = Chit.objects.filter(end_date__gte=date.today())
#     lst=[]
#     for x in chitobj:
#         lst.append(x.id)
#     lst2 = []
#     for i in chitobj2:
#         lst2.append(i.id)
#     obj=Customerchit.objects.filter(Q(chitid_id__in=lst) & Q(status="pending"))
#     obj2 = Customerchit.objects.filter(Q(chitid_id__in=lst) & Q(status="approved"))
#     context={'pending':obj,'approved':obj2}
#     return render(request, 'bankstaff/sample.html',context)


def view_sample(request):
    chitobj=Chit.objects.filter(due_date__gte=date.today())
    chitobj2 = Chit.objects.filter(Q(start_date__lte=date.today()) & Q(end_date__gte=date.today()) )
    context={'chitobj':chitobj,'chitobj2':chitobj2}

    return render(request, 'bankstaff/staffviewchits.html',context)

def viewpendingchitrequests(request,reqid):
    # chitobj = Chit.objects.filter(due_date__gte=date.today())
    # chitobj2 = Chit.objects.filter(end_date__gte=date.today())
    # lst = []
    # for x in chitobj:
    #     lst.append(x.id)
    # lst2 = []
    # for i in chitobj2:
    #     lst2.append(i.id)
    request.session['chitid']=reqid
    obj = Customerchit.objects.filter(Q(chitid_id=reqid) & Q(status="pending"))
    obj2 = Customerchit.objects.filter(Q(chitid_id=reqid) & Q(status="approved"))
    context = {'pending': obj, 'approved': obj2}


    return render(request, 'bankstaff/sample.html', context)


def approvechitrequest(request,reqid):
    chitid=request.session['chitid']
    obj=Customerchit.objects.get(id=reqid)
    obj.status="approved"
    obj.save()
    tamnt=Customerchit.objects.get(id=reqid).chitid.chit_amount
    period=Customerchit.objects.get(id=reqid).chitid.period
    print(tamnt,period)
    pamnt=int(tamnt)/int(period)
    print(tamnt, period,pamnt)
    installmentobj=Installment()
    installmentobj.cust_chitid_id=Customerchit.objects.get(id=reqid).id
    installmentobj.amount=pamnt
    installmentobj.save()
    url = '/staff/viewpendingchitrequests/'+str(chitid)+'/'
    resp_body = '<script>alert("Successfully accepted..");\
                                                                                                 window.location="%s"</script>' % url
    return HttpResponse(resp_body)


def rejectchitrequest(request,reqid):
    chitid = request.session['chitid']
    obj=Customerchit.objects.get(id=reqid)
    obj.status="rejected"
    obj.save()
    url = '/staff/viewpendingchitrequests/'+str(chitid)+'/'
    resp_body = '<script>alert("Successfully rejected..");\
                                                                                                 window.location="%s"</script>' % url
    return HttpResponse(resp_body)

def viewpjoinedchitrequests(request,reqid):
    obj=Customerchit.objects.filter(chitid_id=reqid)
    context={'joined':obj}
    return render(request, 'bankstaff/sample2.html', context)

def addnewmembertochit(request,reqid):
    request.session['chittyId']=reqid
    currentlist = []
    chitperiod = Chit.objects.get(id=reqid).period
    # print(chitperiod)
    numbers = list(range(1, chitperiod + 1))
    custchit = Customerchit.objects.filter(chitid_id=reqid)
    # print(custchit)
    for x in custchit:
        currentlist.append(x.chittal_number)
    # print("not available",currentlist)
    available_list = list(filter(lambda x: x not in currentlist, numbers))
    return render(request, 'bankstaff/accnoinput.html', {'available_list': available_list})

def submitnewmembertochit(request):
    accno = request.POST['accno']
    chittalno = request.POST['chittalno']
    chitId=request.session['chittyId']
    print(accno)
    if not Account.objects.filter(id=accno).exists():
        message = "Account not found..."
        return render(request, 'bankstaff/usernotfound.html', {'message': message,'chitId':chitId})
    else:
        request.session['accNO']=accno
        request.session['chittalNO']=chittalno
        # custchitobj=Customerchit()
        # custchitobj.status="approved"
        # custchitobj.account_number_id=accno
        # custchitobj.chittal_number=chittalno
        # custchitobj.current_payment_count=0
        # custchitobj.chitid_id=chitId
        # custchitobj.save()
        accountrequest=Account.objects.get(id=accno)
        return render(request,'bankstaff/confrimuserandsubmit.html',{'accountrequest':accountrequest})
        # url = 'view_sample'
        # resp_body = '<script>alert("Successfully addded");\
        #                            window.location="%s"</script>' % url
        # return HttpResponse(resp_body)

def confirmnewmembertochit(request):
    accno=request.session['accNO']
    chittalno=request.session['chittalNO']
    chitId=request.session['chittyId']
    custchitobj = Customerchit()
    custchitobj.status = "approved"
    custchitobj.account_number_id = accno
    custchitobj.chittal_number = chittalno
    custchitobj.current_payment_count = 0
    custchitobj.chitid_id = chitId
    custchitobj.save()
    url='view_sample'
    resp_body = '<script>alert("Successfully addded");\
                               window.location="%s"</script>' % url
    return HttpResponse(resp_body)

def staffviewauctionresults(request,reqid):
    auctionobj=Auction.objects.filter(chitid_id=reqid)
    auctionid=[]
    print(auctionobj)
    for i in auctionobj:
        auctionid.append(i.id)
    print(auctionid)
    cname=Chit.objects.get(id=reqid).name
    rslt=Result.objects.filter(auction_id_id__in=auctionid).order_by('-id')
    print(rslt)
    context={'rslt':rslt,'cname':cname}
    return render(request, 'bankstaff/staffviewauctionresults.html',context)

def viewpendingpayments(request,reqid):
    # print(reqid)
    chitregobj=Customerchit.objects.filter(chitid_id=reqid)
    # print(chitregobj)
    pk_list = chitregobj.values_list('pk', flat=True)
    # print(pk_list)
    pk_list=list(pk_list)
    # print(pk_list)
    import datetime
    import calendar
    duedate=Chit.objects.get(id=reqid).pay_due_date
    due_date = datetime.date(datetime.date.today().year, datetime.date.today().month, int(duedate))

    # print the result
    # print("Due date:", due_date)

    # get today's date
    today = datetime.date.today()
    first_day = datetime.date(today.year, today.month, 1)
    # get the last day of the month
    last_day = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    # print("Ending date of the month:", last_day)
    payment_done = Payment.objects.filter(
        Q(cust_chitid__id__in=pk_list) &
        Q(created_at__gte=first_day) & Q(created_at__lte=last_day)
    ).distinct()
    # print(payment_done)
    paid_chit_pks = list(payment_done.values_list('cust_chitid__pk', flat=True).distinct())

    # print("paid chit pks:", paid_chit_pks)
    unpaid_chit_pks = [pk for pk in pk_list if pk not in paid_chit_pks]
    # print("Unpaid chit pks:", unpaid_chit_pks)
    pendingcustomerobj=Customerchit.objects.filter(id__in=unpaid_chit_pks)
    # print(pendingcustomerobj)
    chit=Chit.objects.get(id=reqid)
    #sessioned id's unpaid
    request.session['unpaid_chit_pks'] = json.dumps(unpaid_chit_pks)
    context={'pendingcustomerobj':pendingcustomerobj,'chit':chit}
    return render(request, 'bankstaff/pendingpayment.html',context)

def sendnotification(request):
    unpaid_chit_pks = json.loads(request.session.get('unpaid_chit_pks', '[]'))
    print("***",unpaid_chit_pks)
    phone_number_list=[]
    for i in unpaid_chit_pks:
        customer_chit_obj = Customerchit.objects.get(id=i)
        phone_number_list.append(customer_chit_obj.account_number.accrid.uid.phone)
    print(phone_number_list)
    smsmsg = "Your payment for chit of this month is pending : "
    account_sid = 'AC8bb9a55c8e2e83a3aec7a1af351d600b'
    auth_token = '5974a20ad0f76d34c634ed0bdd3561b0'
    client = Client(account_sid, auth_token)
    # for phone_number in phone_number_list:
    #     mob = '+91' + str(phone_number)
    #     try:
    #         message = client.messages.create(
    #             body=smsmsg,
    #             from_='+16829002201',
    #             to=mob
    #         )
    #     except Exception as e:
    #         print(f"Failed to send message to {phone_number}: {e}")
    url = 'view_sample'
    resp_body = '<script>alert("Successfully notified");\
                                   window.location="%s"</script>' % url
    return HttpResponse(resp_body)

