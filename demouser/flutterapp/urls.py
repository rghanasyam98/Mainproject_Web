from django.urls import path
from  .import views

urlpatterns = [
    path('Customerregister/', views.Customerregister.as_view(), name='Customerregister'),
    path('userlogin/', views.userlogin, name='userlogin'),
    path('userlogout/', views.userlogout, name='userlogout'),
    # path('Accountrequest/', views.Accountrequest.as_view(), name='Accountrequest'),
    path('accountrequest/', views.accountrequest, name='accountrequest'),
    path('accountlink/', views.accountlink, name='accountlink'),
    path('accountadd/<int:rid>/', views.accountadd, name='accountadd'),
    # path('accountadd/', views.accountadd, name='accountadd'),
    path('accountaddcheck/', views.accountaddcheck, name='accountaddcheck'),
    path('getinfoforinitialize/', views.getinfoforinitialize, name='getinfoforinitialize'),
    path('getprofile/', views.getprofile, name='getprofile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('getnews/', views.getnews, name='getnews'),
    path('getloans/', views.getloans, name='getloans'),
    path('loanrequest/', views.loanrequest, name='loanrequest'),
    path('getappliedloan/', views.getappliedloan, name='getappliedloan'),
    path('kycupload/', views.kycupload, name='kycupload'),
    path('getchits/', views.getchits, name='getchits'),
    path('getchitalnumbers/', views.getchitalnumbers, name='getchitalnumbers'),
    path('sendchitrequest/', views.sendchitrequest, name='sendchitrequest'),
    path('getappliedchits/', views.getappliedchits, name='getappliedchits'),
    path('getbalance/', views.getbalance, name='getbalance'),
    path('auctionupdate/<int:auction_id>/', views.auctionupdate, name='auctionupdate'),
    path('getauctions/', views.getauctions, name='getauctions'),
    path('getjoinedchits/', views.getjoinedchits, name='getjoinedchits'),
    path('getjoinedchitauctioninfo/<int:custchitid>/', views.getjoinedchitauctioninfo, name='getjoinedchitauctioninfo'),
    path('submitbid/', views.submitbid, name='submitbid'),
    path('get_auction_remaining_seconds/<int:aid>/', views.get_auction_remaining_seconds, name='get_auction_remaining_seconds'),

    # ... other URL patterns ...
]