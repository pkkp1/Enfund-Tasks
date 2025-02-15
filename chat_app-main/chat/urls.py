from django.urls import path , include
from . import views
from users.views import login_page, logout_page, signup_view

urlpatterns = [
     path('', login_page, name="login"),
     path('logout/', logout_page, name="logout"),
     path('signup/', signup_view, name="signup"),
     path('base/', views.base, name='base'),
     path('chat/<str:room_name>/', views.chat_room, name='chat'),
     path('users/', views.user_list, name="user_list"),
     path('delete/', views.delete_all_users, name="delete_all_users"),
     path('frontend/', views.frontend, name="frontend"),
]