from django.urls import path
from . import views

# URLConfiguration (URLConf)
urlpatterns = [
    path('home/',views.home),
    path('hello/', views.say_hello),
    path('test2/', views.testView),
    path('update/', views.print_to_terminal, name='http://127.0.0.1:8000/admin/playground/vessels_in_port/')
]
