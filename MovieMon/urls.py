from django.urls import path
from . import views

app_name = 'MovieMon'
urlpatterns = [
	path('', views.TitleScreen, name='TitleScreen'),
	path('worldmap/', views.Worldmap, name='Worldmap'),
	path('battle/<moviemon_id>/', views.Battle, name='battle'),
	path('moviedex/', views.Moviedex, name='moviedex'),
	path('moviedex/<moviemon>/', views.detail, name='detail'),
	path('options/', views.Option, name='option'),
	path('options/save_game/', views.Save, name='save_game'),
	path('options/load_game/', views.Load, name='load_game'),
]
