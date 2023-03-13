from rest_framework import serializers
from myapp.models import Myuser,Accountrequest

class Customerregisterserializer(serializers.ModelSerializer):
   class Meta:
       model = Myuser
       fields = '__all__'

class Accountrequestserializer(serializers.ModelSerializer):
   class Meta:
       model = Accountrequest
       fields = '__all__'