from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('test/', test, name='test'),
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('', IndexView.as_view()),
    path('new/', NewOrderView.as_view(), name='new_order'),
    path('take/<int:oid>', test, name='take_order'),
    path('edit-page/', views.edit_page, name='edit-page'),
]
