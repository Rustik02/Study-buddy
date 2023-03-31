from django.urls import path

from base.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', login_user, name='login'),
    path('profile/<int:pk>', user_profile, name='profile'),
    path('logout/', logout_user, name='logout'),
    path('register/', registration_user, name='register'),
    path('room_detail/<int:pk>', room_detail, name='room'),
    path('create_room', room_create, name='create-room'),
    path('create-topic', create_topic, name='create-topic'),
    path('update_room/<int:pk>', room_update, name='edit-room'),
    path('delete_room/<int:pk>', room_delete, name='delete-room'),
    path('delete_message/<int:pk>', message_delete, name='delete-message'),
    path('edit-user/<int:pk>', user_edit, name='edit-user'),

]
