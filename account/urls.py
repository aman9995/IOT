from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name= 'index'),
    path('base/', views.base, name='base'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('customer/', views.customer, name='customer'),
    path ('posts/<str:pk>', views.posts, name = 'posts'),
    path('postblog', views.postblog, name = 'postblog'),
    path('logout', views.logout, name = 'logout'),
    path('needyform', views.needyform, name = 'needyform'),
    path('leaderboard', views.leaderboard, name = 'leaderboard'),
    path('needy', views.needy, name = 'needy'),
    path('contact', views.contact, name = 'contact'),
    path('send',views.send, name='send'),
    path('feed', views.feed, name = 'feed')
]