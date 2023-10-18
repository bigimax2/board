from django.urls import path

from kill import views

urlpatterns = [
	path('', views.index, name='index'),
	path('sendComand', views.parser_kill_id, name='parser_kill_id'),
]