from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from twilio.rest import Client
import random
from datetime import datetime,date,timedelta

from django.shortcuts import get_object_or_404
from myapp.models import Myuser, Accountrequest, Account, News, Loan, Customerloan, Kyc, Chit, Customerchit, Auction, \
    Auctionbid, Auctionbidamount,Auctionbidamountlatest
from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
import json
# myapp/views.py
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_jwt.views import ObtainJSONWebToken
from django.db.models import Q
import base64
import jwt
from datetime import datetime, timedelta
from django.conf import settings

from django.conf import settings
from flutterapp.serializers import Customerregisterserializer, Accountrequestserializer


class Customerregister(generics.GenericAPIView):
    serializer_class = Customerregisterserializer
    def post(self,request,format=None):
        print("hai")
        body = request.body.decode('utf-8')
        data = json.loads(body)
        print(data)
        mail=data['email']
        print('mail',mail)
        phone=data['phone']
        password=data['password']
        p = make_password(password)
        em = Myuser.objects.filter(email=mail)
        print(em)
        print(len(em))
        if len(em) == 0:
            # mail=request.data.get('email')
            # phone = request.data.get('phone')
            # password = request.data.get('password')
            # print(mail,phone,password)

            # serializer = self.serializer_class(data={'email':'abi123@gmail.com','phone':'9999999999','password':'ghanasyam','username':'ghanasyam1','first_name':'shyam','last_name':'shyam','user_type':'customer'})

            serializer = self.serializer_class(
                data={'email': mail, 'phone': phone, 'password': p, 'username': mail, 'first_name': 'shyam',
                      'last_name': 'shyam', 'user_type': 'customer'})
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def userlogin(request):
    print("login")
    # email = request.data.get('email')
    # password = request.data.get('password')
    body = request.body.decode('utf-8')
    data = json.loads(body)
    # print(data)
    mail=data['email']
    password=data['password']
    # print(mail,password)
    try:
        usr = Myuser.objects.get(Q(email=mail) & Q(user_type="customer"))
    except :
        usr = None
    # print(usr.email)
    user = authenticate(username=usr.email, password=password)
    # print(user)
    if user is not None:
        # jwt_view = ObtainJSONWebToken.as_view()
        # response = jwt_view(request)
        # print(response)
        login(request, user)
        print(user.id)
        request.session['userid'] = user.id
        token=generate_jwt_token(user)
        # print('token',token)
        # return response
        # return Response({'token': token})
        return Response({'token': token,'mail':user.username}, status=status.HTTP_201_CREATED)

        # return Response({'message': 'success'}, status=status.HTTP_201_CREATED)

    else:
        return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)



def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def userlogout(request):
    # print(request.user)
    token = request.headers.get('Authorization', '')
   # userid = request.session['userid']
    # print(token)
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = decoded_token.get('user_id')
    # print(user_id)
    # print(request.session)
    logout(request)
    request.session.flush()
    if 'sessionid' not in request.COOKIES:
        # User is logged out
        print('111')
        return Response({'message': 'Successfully logged out'},status=status.HTTP_201_CREATED)
    else:
        # Logout failed
        return Response({'error': 'failed'}, status=status.HTTP_401_UNAUTHORIZED)
    # request.user.auth_token.delete()



# class Accountrequest(generics.GenericAPIView):
#     serializer_class = Accountrequestserializer
#     def post(self,request,format=None):
#         # body = request.body.decode('utf-8')
#         body = request.body.decode('iso-8859-1')
#         # data = json.loads(body)
#         # print(data)
#         delimiter = ','
#         substrings = body.split(delimiter)
#
#         # Extract fields from the list
#         field1 = substrings[0]
#         field2 = substrings[1]
#         field3 = substrings[2]
#         print(field1,field3,field3)
#         token = request.headers.get('Authorization', '')
#         # userid = request.session['userid']
#         # print(token)
#         # decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#         # user_id = decoded_token.get('user_id')
#         # fname = data['fname']
#         # lname = data['lname']
#         # gender = data['gender']
#         # dob = data['dob']
#         # address = data['address']
#         # marital_status = data['marital_status']
#         # nameof_fms = data['nameof_fms']
#         # dependants = data['dependants']
#         # nation = data['nameof_fms']
#         # employment = data['nameof_fms']
#         # income = data['income']
#         # graduation = data['graduation']
#         # property = data['property']
#         # account = data['account']
#         # nominee = data['nominee']
#         # nomaddress = data['nomaddress']
#         # relation = data['relation']
#         # aadhar = data['aadhar']
#         # image = data['image']
#
#
#
#         # image_bytes = base64.b64decode(image)
#         # print(image_bytes)
#         # with open('media/images/img1.jpg', 'wb') as f:
#         #     f.write(image_bytes)
#         # serializer = self.serializer_class(
#         #     data={'fname':fname,'lname':lname,'gender':gender,'dob':dob,'address':address,
#         #           'marital_status':marital_status,'namefms':nameof_fms,'dependants':dependants,
#         #           'nationality':nation,'occupation':employment,'income':income,'qualification':graduation,
#         #           'type':account,'pan':property,'aadhar':aadhar,'nomname':nominee,'nomaddress':nomaddress,'relation':relation,
#         #          'status':"pending",'image':"afgdjhfkklglgl" ,'uid':user_id})
#         serializer = self.serializer_class(
#             data={'fname': 'aa', 'lname': 'aa', 'gender': 'male', 'dob': '1998-07-19', 'address':'aaaa',
#                   'marital_status': 'yes', 'namefms': 'aaa', 'dependants':1 ,
#                   'nationality': 'aa', 'occupation': 'aa', 'income': '122', 'qualification': 'graduation',
#                   'type': 'account', 'pan': 'property', 'aadhar': 'aadhar', 'nomname': 'nominee', 'nomaddress': 'nomaddress',
#                   'relation': 'relation',
#                   'status': "pending", 'image': "afgdjhfkklglgl", 'uid':17})
#         # print(serializer)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

@csrf_exempt
def accountrequest(request):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        # auth_header = request.META.get('Authorization')
        print(auth_header)
        decoded_token = jwt.decode(auth_header, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        print(user_id)
        obj=Accountrequest.objects.filter(uid=user_id,status="pending").exists()
        if obj:
            print("already exists")
            data = {'status': 'failure'}
            status_code = 409
            return JsonResponse(data, status=status_code)

        image_file = request.FILES.get('image')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        marital_status = request.POST.get('marital_status')
        nameof_fms = request.POST.get('nameof_fms')
        dependants = request.POST.get('dependants')
        nation = request.POST.get('nation')
        employment = request.POST.get('employment')
        income = request.POST.get('income')

        property = request.POST.get('property')
        graduation = request.POST.get('graduation')
        account = request.POST.get('account')
        nominee = request.POST.get('nominee')
        nomaddress = request.POST.get('nomaddress')
        relation = request.POST.get('relation')
        aadhar = request.POST.get('aadhar')
        # print(image_file.name)
        # fs = FileSystemStorage()
        # filename = fs.save(image_file.name, image_file)
        # uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        # return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
        if gender=='0':
            gender="Male"
        else:
            gender="Female"
        datetime_obj = datetime.strptime(dob, '%Y-%m-%d %H:%M:%S.%f')  # convert string to datetime object
        date_only = datetime_obj.date()
        dependants=dependants.replace('+', '')
        print(dependants)
        print(fname,lname,image_file,gender,date_only,address,marital_status,nameof_fms,dependants,nation,employment,income,graduation,property,graduation,account,nominee,nomaddress,relation,aadhar)

        acc_requestobj=Accountrequest()
        acc_requestobj.fname=fname
        acc_requestobj.lname=lname
        acc_requestobj.gender=gender
        acc_requestobj.dob=date_only
        acc_requestobj.address=address
        acc_requestobj.marital_status=marital_status
        acc_requestobj.namefms=nameof_fms
        acc_requestobj.dependants=dependants
        acc_requestobj.nationality=nation
        acc_requestobj.occupation=employment
        acc_requestobj.income=income
        acc_requestobj.qualification=graduation
        acc_requestobj.type=account
        acc_requestobj.pan=property
        acc_requestobj.nomname=nominee
        acc_requestobj.nomaddress=nomaddress
        acc_requestobj.relation=relation
        acc_requestobj.aadhar=aadhar
        acc_requestobj.image=image_file
        acc_requestobj.status="pending"
        acc_requestobj.uid_id=int(user_id)
        acc_requestobj.save()
        data = {'status': 'success'}
        status_code = 200
        return JsonResponse(data, status=status_code)


@csrf_exempt
def accountlink(request):
    if request.method == 'POST':
        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        decoded_token = jwt.decode(auth_header, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        # print(user_id)
        accno = request.POST.get('accno')
        # print(accno)
        obj=Account.objects.filter(id=accno)
        # print(obj)

        if obj:
            myobj=Account.objects.filter( id=accno).order_by('-id').last()
            account_requestid=myobj.accrid.id
            Accobj=Accountrequest.objects.filter(id=account_requestid).order_by('-id').last()
            account_requestuid = Accobj.uid.id
            if Accountrequest.objects.get(id=account_requestid).status=="added":
                data = {'status': 'failure'}
                status_code = 401
                return JsonResponse(data, status=status_code)

            print(account_requestuid)
            phone=Myuser.objects.get(id=account_requestuid).phone
            print(phone)

            random_number = random.randint(100000, 999999)
            print(myobj.accrid.id)
            request.session['account_request_id']=myobj.accrid.id
            print(random_number)
            # mob = '+91' + str(phone)
            # smsmsg ="Your OTP for verification is : "+ str(random_number)
            # account_sid = 'AC8bb9a55c8e2e83a3aec7a1af351d600b'
            # auth_token = '6543e661182f0c1f5fccf34e70449896'
            # client = Client(account_sid, auth_token)
            # try:
            #     message = client.messages.create(
            #
            #         body=smsmsg,
            #         from_='+16829002201',
            #         to=mob
            #
            #     )
            # except:
            #     data = {'status': 'failure'}
            #     status_code = 403


            data = {'status': 'success','otp':random_number,'account_requestid':myobj.accrid.id}
            status_code = 200
        else:
            data = {'status': 'failure'}
            status_code = 400
        return JsonResponse(data, status=status_code)



@csrf_exempt
def accountadd(request,rid):
    if request.method == 'POST':
        # account_request_id = request.session.get('account_request_id')
        print("from url",rid)
        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        decoded_token = jwt.decode(auth_header, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        print(user_id)
        acc_reqid = request.POST.get('acc_reqid')
        print('from body',acc_reqid)
        accobj=Accountrequest.objects.get(id=rid)
        accobj.status="added"
        accobj.save()
        obj2=Account.objects.get(accrid_id=rid).id
        print(obj2)
        data = {'status': 'success','accno':obj2}
        status_code = 200
        return JsonResponse(data, status=status_code)



@csrf_exempt
def accountaddcheck(request):
    if request.method == 'POST':
        print("entered")
        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        decoded_token = jwt.decode(auth_header, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if Accountrequest.objects.filter(uid_id=user_id):
            accreqobj = Accountrequest.objects.get(uid_id=user_id).status
            if accreqobj == "added":
                data = {'status': 'success'}
                status_code = 200
            else:
                data = {'status': 'failure'}
                status_code = 400
        else:
            data = {'status': 'failure'}
            status_code = 400
        return JsonResponse(data, status=status_code)


@csrf_exempt
def getinfoforinitialize(request):
    if request.method == 'POST':
        print("getinfoforinitialize")

        auth_header = request.headers.get('Authorization')
        # print(auth_header)
        decoded_token = jwt.decode(auth_header, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if Accountrequest.objects.filter(uid_id=user_id):
            accreqobj = Accountrequest.objects.get(uid_id=user_id).status
            if accreqobj == "added":
                reqid = Accountrequest.objects.get(uid_id=user_id).id
                accholdername = Accountrequest.objects.get(uid_id=user_id).fname
                acctype = Accountrequest.objects.get(uid_id=user_id).type
                phone = Myuser.objects.get(id=user_id).phone
                mail = Myuser.objects.get(id=user_id).email
                accno = Account.objects.get(accrid_id=reqid).id
                print(accholdername, acctype, accno)
                data = {'status': 'success', 'accno': accno, 'accholdername': accholdername, 'acctype': acctype,'phone':phone,'mail':mail}
                status_code = 200
            else:
                phone = Myuser.objects.get(id=user_id).phone
                mail = Myuser.objects.get(id=user_id).email
                data = {
                    'phone': phone, 'mail': mail}

                status_code = 400


        else:
            data = {'status': 'failure'}
            status_code = 204

        return JsonResponse(data, status=status_code)


@csrf_exempt
def getprofile(request):
    if request.method == 'POST':
        accno = request.POST.get('accno')
        print(accno)

        if Account.objects.get(id=accno).accrid:
            reqid = Account.objects.get(id=accno).accrid_id
            profileinfo=Accountrequest.objects.get(id=reqid)
            print(profileinfo)
            imgurl=profileinfo.image
            print(imgurl)
            data={'maritalstatus':profileinfo.marital_status,'dependants':profileinfo.dependants,'employment':profileinfo.occupation,
                  'graduationstatus':profileinfo.qualification,'property':profileinfo.pan,'address':profileinfo.address,'income':profileinfo.income,
                 'image':str(imgurl)
                  }
            print(data)

            # data = {'status': 'success',}
            status_code = 200
            return JsonResponse(data, status=status_code)
            # return JsonResponse(serialized_data, safe=False, status=200)

        else:
            data = {'status': 'failure'}
            status_code = 204
            return JsonResponse(data, status=status_code)




@csrf_exempt
def updateprofile(request):
    if request.method == 'POST':
        accno = request.POST.get('accno')
        print(accno)

        if Account.objects.get(id=accno).accrid:
            reqid = Account.objects.get(id=accno).accrid_id
            if request.POST.get('image')== "notnull":
                image_file = request.FILES.get('image')
            else:
                image_file=None


            address = request.POST.get('address')
            marital_status = request.POST.get('marital_status')

            dependants = request.POST.get('dependants')

            employment = request.POST.get('employment')
            income = request.POST.get('income')

            property = request.POST.get('property')
            graduation = request.POST.get('graduation')
            print(address,marital_status,dependants,employment,income,property,graduation,image_file)
            # print(image_file.name)
            # fs = FileSystemStorage()
            # filename = fs.save(image_file.name, image_file)
            # uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url)
            # return Response({'message': 'success'}, status=status.HTTP_201_CREATED)


            dependants = dependants.replace('+', '')
            print(dependants)
            acc_requestobj = Accountrequest.objects.get(id=reqid)

            acc_requestobj.address = address
            acc_requestobj.marital_status = marital_status

            acc_requestobj.dependants = dependants

            acc_requestobj.occupation = employment
            acc_requestobj.income = income
            acc_requestobj.qualification = graduation

            acc_requestobj.pan = property
            if image_file is not None:
                acc_requestobj.image = image_file
            acc_requestobj.save()
            data = {'status': 'success'}
            status_code = 200
        else:
            data = {'status': 'failure'}
            status_code = 204
        return JsonResponse(data, status=status_code)


@csrf_exempt
def getnews(request):
    if request.method == 'POST':
        news=News.objects.all().order_by('-id')
        serialized_data = list(news.values())
        print(serialized_data)# convert queryset to list of dictionaries
        return JsonResponse(serialized_data, safe=False, status=200)

@csrf_exempt
def getloans(request):
    if request.method == 'POST':
        loans=Loan.objects.all()
        serialized_data = list(loans.values())
        print(serialized_data)  # convert queryset to list of dictionaries
        return JsonResponse(serialized_data, safe=False, status=200)



@csrf_exempt
def loanrequest(request):
    if request.method == 'POST':
        accno = request.POST.get('accno')
        amount = request.POST.get('amount')
        loanid = request.POST.get('loanid')
        loan = Customerloan.objects.filter(account_number_id=accno, loanid_id=loanid).first()
        # loan = get_object_or_404(Loan, account_number=accno, loanid=loanid)
        if loan:
            if loan.status=="pending":
                data = {'status': 'failure'}
                status_code = 204
                return JsonResponse(data, status=status_code)




        print(loan)

        print(accno,amount,loanid)
        obj=Customerloan()
        obj.loan_amount=amount
        obj.status="pending"
        obj.account_number_id=accno
        obj.loanid_id=int(loanid)
        obj.save()
        data = {'status': 'success'}
        status_code = 200
        return JsonResponse(data, status=status_code)


#
# @csrf_exempt
# def getappliedloan(request):
#     if request.method == 'POST':
#         accno = request.POST.get('accno')
#         loans = Customerloan.objects.filter(account_number_id=accno,)
#         loan_list_size = len(loans)
#         loan_list = [None] * loan_list_size
#         for i, x in enumerate(loans):
#             loan_dict = x.__dict__
#             loan_dict['loan_name'] = x.loanid.lname
#             loan_dict['date'] = x.created_at.date()
#             loan_dict['amount'] = x.loan_amount
#             loan_dict['amount'] = x.status
#             if x.max_date is None:
#                 loan_dict['max'] = 'will be informed'
#             else:
#                 loan_dict['max'] = x.max_date
#             if x.min_date is None:
#                 loan_dict['min'] = 'will be informed'
#             else:
#                 loan_dict['min'] = x.min_date
#             if x.emi is None:
#                 loan_dict['emi'] = 'will be informed'
#             else:
#                 loan_dict['emi'] = x.emi
#             loan_list[i] = loan_dict
#         # serialized_data = loan_list
#         serialized_data = list(loan_list)
#         print(serialized_data)  # convert queryset to list of dictionaries
#         return JsonResponse(serialized_data, safe=False, status=200)


@csrf_exempt
def getappliedloan(request):
    if request.method == 'POST':
        accno = request.POST.get('accno')
        loans = Customerloan.objects.filter(account_number_id=accno)
        loan_list_size = len(loans)
        loan_list = [None] * loan_list_size
        for i, x in enumerate(loans):
            loan_dict = {
                'loan_name': x.loanid.lname,
                'date': x.created_at.date(),
                'amount': x.loan_amount,
                'status': x.status,
                'max': 'will be informed' if x.max_date is None else x.max_date,
                'min': 'will be informed' if x.min_date is None else x.min_date,
                'emi': 'will be informed' if x.emi is None else x.emi,
            }
            loan_list[i] = loan_dict
        serialized_data = loan_list
        print(serialized_data)  # convert queryset to list of dictionaries
        return JsonResponse(serialized_data, safe=False, status=200)




@csrf_exempt
def kycupload(request):
    if request.method == 'POST':
        accno = request.headers.get('accno')
        doc_file = request.FILES.get('doc')
        doc_file2 = request.FILES.get('doc2')
        print(accno,doc_file,doc_file2)
        # obj=Kyc.objects.get(account_number_id=int(accno))
        # print(obj)
        if Kyc.objects.filter(account_number_id=int(accno)).exists():
            data = {'status': 'failure'}
            status_code = 204
            return JsonResponse(data, status=status_code)
        kyc=Kyc()
        kyc.account_number_id=int(accno)
        kyc.form=doc_file
        kyc.proof=doc_file2
        kyc.save()
        data = {'status': 'success'}
        status_code = 200
        return JsonResponse(data, status=status_code)
    data = {'status': 'failure'}
    status_code = 400
    return JsonResponse(data, status=status_code)


@csrf_exempt
def getchits(request):
    if request.method == 'POST':
        current_date = date.today()
        chits=Chit.objects.filter(due_date__gte=current_date).order_by('-id')
        serialized_data = list(chits.values())
        print(serialized_data)  # convert queryset to list of dictionaries
        return JsonResponse(serialized_data, safe=False, status=200)



@csrf_exempt
def getchitalnumbers(request):
    if request.method == 'POST':
        currentlist=[]
        chitid = request.POST.get('chitid')
        # print(chitid)
        chitperiod=Chit.objects.get(id=chitid).period
        # print(chitperiod)
        numbers = list(range(1, chitperiod+1))
        custchit=Customerchit.objects.filter(chitid_id=chitid)
        # print(custchit)
        for x in custchit:
            currentlist.append(x.chittal_number)
        # print("not available",currentlist)
        available_list = list(filter(lambda x: x not in currentlist, numbers))
        if len(available_list)==0:
            data = {'status': 'failure'}
            status_code = 400
            return JsonResponse(data, status=status_code)
        # print("available",available_list)
        # print("all",numbers)
        my_dict_list = [{"available_id": i+1} for i, x in enumerate(available_list)]
        print(my_dict_list)
        return JsonResponse(available_list, safe=False, status=200)
        # data = {'status': 'success'}
        # status_code = 200
        # return JsonResponse(data, status=status_code)



@csrf_exempt
def sendchitrequest(request):
    if request.method == 'POST':
        chitid = request.POST.get('chitid')
        chittalnumber = request.POST.get('chitalnumber')
        accno = request.POST.get('accno')
        print(chitid,chittalnumber,accno)
        chk = Customerchit.objects.filter(account_number_id=accno, chitid_id=chitid).first()
        # loan = get_object_or_404(Loan, account_number=accno, loanid=loanid)
        if chk:
            if chk.status == "pending":
                data = {'status': 'failure'}
                status_code = 204
                return JsonResponse(data, status=status_code)
        obj=Customerchit()
        obj.chittal_number=int(chittalnumber)
        obj.account_number_id=int(accno)
        obj.chitid_id=chitid
        obj.status="pending"
        obj.current_payment_count=0
        obj.save()
        data = {'status': 'success'}
        status_code = 200
        return JsonResponse(data, status=status_code)
    data = {'status': 'failure'}
    status_code = 400
    return JsonResponse(data, status=status_code)



@csrf_exempt
def getappliedchits(request):
    if request.method == 'POST':
        print("****")
        accno = request.POST.get('accno')
        chits = Customerchit.objects.filter(account_number_id=accno)
        chit_list_size = len(chits)
        chit_list = [None] * chit_list_size
        for i, x in enumerate(chits):
            chit_dict = {
                'id': x.id,
                'chit_name': x.chitid.name,
                'amount': x.chitid.chit_amount,
                'period': x.chitid.period,
                'status': x.status,
                'start': x.chitid.start_date,
                'end': x.chitid.end_date,
                'paydue':x.chitid.pay_due_date,
                'current_installment': x.current_payment_count,
                'chittal_number':x.chittal_number
            }
            chit_list[i] = chit_dict
        serialized_data = chit_list
        print(serialized_data)  # convert queryset to list of dictionaries
        return JsonResponse(serialized_data, safe=False, status=200)

@csrf_exempt
def getbalance(request):
    if request.method == 'POST':
        print("****")
        accno = request.POST.get('accno')
        print(accno)
        data = {'balance': Account.objects.get(id=accno).balance}
        status_code = 200
        return JsonResponse(data, status=status_code)
    data = {'status': 'failure'}
    status_code = 400
    return JsonResponse(data, status=status_code)

# @csrf_exempt
# def auctionupdate(request,auction_id):
#     if request.method == 'POST':
#         print("auction")
#         bidamount = Auctionbidamountlatest.objects.filter(auction_id_id=auction_id).order_by('amount').values()[:3]
#         bidamounttop = Auctionbidamountlatest.objects.filter(auction_id_id=auction_id).order_by('amount')
#         # created=bidamounttop[0].created_at
#         created = timezone.localtime(bidamounttop[0].created_at)
#         time_difference = datetime.now() - created
#         third_call = False
#         second_call = False
#         first_call = False
#         # Check if the time difference is greater than 3 minutes
#         if time_difference > timedelta(minutes=3):
#             third_call = True
#             second_call = True
#             first_call = True
#         # Check if the time difference is greater than 2 minutes and less than or equal to 3 minutes
#         elif time_difference > timedelta(minutes=2):
#             third_call = False
#             second_call = True
#             first_call = True
#         # Check if the time difference is greater than 1 minute and less than or equal to 2 minutes
#         elif time_difference > timedelta(minutes=1):
#             third_call = False
#             second_call = False
#             first_call = True
#         # The time difference is less than or equal to 1 minute
#         else:
#             third_call = False
#             second_call = False
#             first_call = False
#
#
#         # data = {'bidamount': list(bidamount.values())}
#         data = {'bidamount': list(bidamount.values()), 'third_call': third_call, 'second_call': second_call, 'first_call': first_call}
#
#         print(data)
#         # data = {'min_bid_amount': time_str}
#         status_code = 200
#         return JsonResponse(data, status=status_code)

@csrf_exempt
def auctionupdate(request,auction_id):
    if request.method == 'POST':
        print("auction")
        bidamount = Auctionbidamountlatest.objects.filter(auction_id_id=auction_id).order_by('amount').values()[:3]
        bidamounttop = Auctionbidamountlatest.objects.filter(auction_id_id=auction_id).order_by('amount')
        created = bidamounttop[0].created_at
        created = timezone.localtime(created)
        time_difference = timezone.now() - created
        third_call = False
        second_call = False
        first_call = False
        # Check if the time difference is greater than 3 minutes
        if time_difference > timedelta(minutes=3):
            third_call = True
            second_call = True
            first_call = True
        # Check if the time difference is greater than 2 minutes and less than or equal to 3 minutes
        elif time_difference > timedelta(minutes=2):
            third_call = False
            second_call = True
            first_call = True
        # Check if the time difference is greater than 1 minute and less than or equal to 2 minutes
        elif time_difference > timedelta(minutes=1):
            third_call = False
            second_call = False
            first_call = True
        # The time difference is less than or equal to 1 minute
        else:
            third_call = False
            second_call = False
            first_call = False

        data = {'bidamount': list(bidamount.values()), 'third_call': third_call, 'second_call': second_call, 'first_call': first_call}
        print(data)
        status_code = 200
        return JsonResponse(data, status=status_code)


@csrf_exempt
def getauctions(request):
    if request.method == 'POST':
        print("view auctions")
        accno = request.POST.get('accno')
        print(accno)
        chitobj=Customerchit.objects.filter(account_number_id=accno)
        lst=[]
        for x in chitobj:
            lst.append(x.chitid_id)
        print(lst)
        auctionobj=Auction.objects.filter(chitid_id__in=lst)
        print(auctionobj)

        status_code = 200
        data = {'status': 'success'}
        return JsonResponse(data, status=status_code)
    data = {'status': 'failure'}
    status_code = 400
    return JsonResponse(data, status=status_code)


@csrf_exempt
def getjoinedchits(request):
    if request.method == 'POST':
        print("****")
        accno = request.POST.get('accno')
        chits = Customerchit.objects.filter(account_number_id=accno,status="approved")
        chit_list_size = len(chits)
        chit_list = [None] * chit_list_size
        for i, x in enumerate(chits):
            chit_dict = {
                'id' : x.id,
                'chit_name': x.chitid.name,
                'amount': x.chitid.chit_amount,
                'period': x.chitid.period,
                'status': x.status,
                'start': x.chitid.start_date,
                'end': x.chitid.end_date,
                'paydue':x.chitid.pay_due_date,
                'current_installment': x.current_payment_count,
                'chittal_number':x.chittal_number
            }
            chit_list[i] = chit_dict
        serialized_data = chit_list
        print(serialized_data)  # convert queryset to list of dictionaries
        return JsonResponse(serialized_data, safe=False, status=200)


@csrf_exempt
def getjoinedchitauctioninfo(request, custchitid):
    if request.method == 'POST':
        print(custchitid)
        chitid=Customerchit.objects.get(id=custchitid).chitid_id
        auctionobj=Auction.objects.filter(chitid_id=chitid).order_by("-id")
        print(auctionobj)
        serialized_data = list(auctionobj.values())
        print(serialized_data)  # convert que
        status_code = 200
        data = {'status': 'success'}
        print(serialized_data)  # convert queryset to list of dictionaries
        return JsonResponse(serialized_data, safe=False, status=200)
    data = {'status': 'failure'}
    status_code = 400
    return JsonResponse(data, status=status_code)


@csrf_exempt
def submitbid(request):
    if request.method == 'POST':
        custchitid = request.POST.get('custchitid')
        auctionid = request.POST.get('auctionid')
        amount= request.POST.get('amount')
        print(custchitid,auctionid,amount)
        bidobj=Auctionbidamountlatest()
        bidobj.auction_id_id=int(auctionid)
        bidobj.cust_chitid_id=int(custchitid)
        bidobj.amount=amount
        bidobj.save()
        status_code = 200
        data = {'status': 'success'}
        return JsonResponse(data, status=status_code)
    data = {'status': 'failure'}
    status_code = 400
    return JsonResponse(data, status=status_code)


# @csrf_exempt
# def get_auction_remaining_seconds(request,aid):
#     if request.method == 'POST':
#         auction = Auction.objects.get(id=aid)
#
#         # Combine the date and time fields to create a datetime object
#         auction_datetime = datetime.combine(auction.auction_date, auction.auction_time)
#
#         # Calculate the time difference between the auction datetime and the current time
#         from django.utils import timezone
#         time_difference = auction_datetime - timezone.now()
#
#         # Convert the time difference to seconds
#         remaining_seconds = time_difference.total_seconds()
#         print("remaining_seconds",remaining_seconds)
#         data = {'remaining_seconds': remaining_seconds}
#         return JsonResponse(data, status=200)
#     data = {'status': 'failure'}
#     status_code = 400
#     return JsonResponse(data, status=status_code)

from django.utils import timezone

#
# @csrf_exempt
# def get_auction_remaining_seconds(request, aid):
#     if request.method == 'POST':
#         auction = Auction.objects.get(id=aid)
#
#         # Combine the date and time fields to create a timezone-aware datetime object
#         auction_datetime = timezone.make_aware(datetime.combine(auction.auction_date, auction.auction_time))
#
#         # Calculate the time difference between the auction datetime and the current time
#         time_difference = auction_datetime - timezone.now()
#
#         # Convert the time difference to seconds
#         # remaining_seconds = time_difference.total_seconds()
#         remaining_seconds = abs(time_difference.total_seconds())
#         print("remaining_seconds", remaining_seconds)
#         data = {'remaining_seconds': remaining_seconds}
#         return JsonResponse(data, status=200)
#
#     data = {'status': 'failure'}
#     status_code = 400
#     return JsonResponse(data, status=status_code)


@csrf_exempt
def get_auction_remaining_seconds(request, aid):
    if request.method == 'POST':
        auction = Auction.objects.get(id=aid)

        # Combine the date and time fields to create a timezone-aware datetime object
        auction_datetime = timezone.make_aware(datetime.combine(auction.auction_date, auction.auction_time))

        # Calculate the time difference between the auction datetime and the current time
        time_difference = auction_datetime - timezone.now()

        # Get the end time of the auction (30 minutes after the starting time)
        auction_end_time = auction_datetime + timedelta(minutes=30)

        # Calculate the time difference between the auction end time and the current time
        remaining_time = auction_end_time - timezone.now()

        # Convert the remaining time to seconds
        remaining_seconds = max(remaining_time.total_seconds(), 0)
        print("remaining_seconds",remaining_seconds)
        data = {'remaining_seconds': remaining_seconds}
        return JsonResponse(data, status=200)

    data = {'status': 'failure'}
    status_code = 400
    return JsonResponse(data, status=status_code)