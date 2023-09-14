
from django.urls import path
from Guest import views
app_name="Guest"
urlpatterns = [
    path('org/',views.neworg,name="neworg"),
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('participate/',views.participate,name="participate"),
    path('interest/',views.interest,name="interest"),
    path('change/interest/',views.change_interest,name="change_interest"),
    path('groups/',views.groups,name="groups"),
]
