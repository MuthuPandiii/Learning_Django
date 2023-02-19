from django.urls import path
from App1 import views

app_name = 'App1'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login')
]
