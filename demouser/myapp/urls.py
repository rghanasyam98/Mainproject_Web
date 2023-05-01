from django.urls import path

from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('login_user', views.login_user, name='login_user'),
     path('logoutadmin', views.logoutadmin, name='logoutadmin'),
     path('admindash', views.admindash, name='admindash'),
     path('staffdash', views.staffdash, name='staffdash'),
     path('loan_management', views.loan_management, name='loan_management'),
     path('addloan', views.addloan, name='addloan'),
     path('getloanfromform', views.getloanfromform, name='getloanfromform'),
     path('update_loan/<int:lid>/',views.update_loan, name='update_loan'),
     path('getupdatedloanfromform', views.getupdatedloanfromform, name='getupdatedloanfromform'),
     path('delete_loan/<int:lid>/',views.delete_loan, name='delete_loan'),
     path('chit_management', views.chit_management, name='chit_management'),
     path('addchit', views.addchit, name='addchit'),
     path('getchitfromform', views.getchitfromform, name='getchitfromform'),
     path('update_chit/<int:cid>/',views.update_chit, name='update_chit'),
     path('getupdatedchitfromform', views.getupdatedchitfromform, name='getupdatedchitfromform'),
     path('delete_chit/<int:cid>/',views.delete_chit, name='delete_chit'),
     path('news_management', views.news_management, name='news_management'),
     path('getnewsfromform', views.getnewsfromform, name='getnewsfromform'),
     path('delete_news/<int:nid>/',views.delete_news, name='delete_news'),
     path('addnews', views.addnews, name='addnews'),
     path('update_news/<int:nid>/',views.update_news, name='update_news'),
     path('getupdatednewsfromform', views.getupdatednewsfromform, name='getupdatednewsfromform'),
     path('auction_management', views.auction_management, name='auction_management'),
     path('addauction', views.addauction, name='addauction'),
     path('getauctionfromform', views.getauctionfromform, name='getauctionfromform'),
     path('delete_auction/<int:aid>/', views.delete_auction, name='delete_auction'),
     path('update_auction/<int:aid>/', views.update_auction, name='update_auction'),
     path('getupdatedauctionfromform', views.getupdatedauctionfromform, name='getupdatedauctionfromform'),

]