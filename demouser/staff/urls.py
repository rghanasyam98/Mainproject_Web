from django.urls import path
from  .import views

urlpatterns = [
    path('view_accountrequests', views.view_accountrequests, name='view_accountrequests'),
    path('accept_accountrequest/<int:reqid>/', views.accept_accountrequest, name='accept-accept_accountrequest'),
    path('reject_accountrequest/<int:reqid>/', views.reject_accountrequest, name='reject_accountrequest'),
    path('view_loanrequests', views.view_loanrequests, name='view_loanrequests'),
    path('viewmoredetailsofloanrequest/<int:reqid>/', views.viewmoredetailsofloanrequest, name='viewmoredetailsofloanrequest'),
    path('reject_loanrequest/<int:reqid>/', views.reject_loanrequest, name='reject_loanrequest'),
    path('listloan', views.listloan, name='listloan'),
    path('approve_loan/<int:reqid>/', views.approve_loan, name='approve_loan'),
    path('view_sample', views.view_sample, name='view_sample'),
    path('viewmoredetailsofloanrequest2/<int:reqid>/', views.viewmoredetailsofloanrequest2, name='viewmoredetailsofloanrequest2'),
    path('viewpendingchitrequests/<int:reqid>/', views.viewpendingchitrequests, name='viewpendingchitrequests'),
    path('approvechitrequest/<int:reqid>/', views.approvechitrequest,name='approvechitrequest'),
    path('rejectchitrequest/<int:reqid>/', views.rejectchitrequest,name='rejectchitrequest'),
    path('viewpjoinedchitrequests/<int:reqid>/', views.viewpjoinedchitrequests, name='viewpjoinedchitrequests'),
    path('addnewmembertochit/<int:reqid>/', views.addnewmembertochit, name='addnewmembertochit'),
    path('submitnewmembertochit', views.submitnewmembertochit, name='submitnewmembertochit'),
    path('confirmnewmembertochit', views.confirmnewmembertochit, name='confirmnewmembertochit'),
    path('staffviewauctionresults/<int:reqid>/', views.staffviewauctionresults, name='staffviewauctionresults'),
    path('viewpendingpayments/<int:reqid>/', views.viewpendingpayments, name='viewpendingpayments'),
    path('sendnotification', views.sendnotification, name='sendnotification'),

]
