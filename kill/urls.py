from django.urls import path

from kill import views

urlpatterns = [
	path('', views.index, name='index'),
]