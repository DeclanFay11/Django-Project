from django.urls import path
from . import views

# URLConfiguration (URLConf)
urlpatterns = [
    path('home/',views.home),
    path('hello/', views.say_hello),
    path('test/', views.testView),
    path('update/', views.print_to_terminal)
]
