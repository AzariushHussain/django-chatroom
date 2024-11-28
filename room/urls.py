from django.urls import path
from .views import room_view, create_room,  messages_view

urlpatterns = [
    path('', room_view, name='room'),
    path('<int:room_id>/', room_view, name='room'),
    path('create/', create_room, name='create_room'),
    path('<int:room_id>/chat', messages_view, name='chat'),
]