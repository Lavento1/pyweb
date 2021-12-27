from django.urls import path
from polls import views

app_name = 'poll'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
]