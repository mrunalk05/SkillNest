from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register, name='register'),
    path('afterLogin', views.afterLogin, name='afterLogin'),
    path('logout', views.handelLogout, name='logout'),
    path('skillPost', views.skillPost, name='skillPost'),
    path('skillview',views.skillview.as_view()),
    path('skillview/<str:pk>',views.skillview.as_view()),
    path('domainview',views.domainview.as_view()),
    path('domainview/<str:pk>',views.domainview.as_view()),
]