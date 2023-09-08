
from django.urls import path
from Organizer  import views
app_name="org"
urlpatterns = [
    path('home/', views.home,name="home"),
    path('event/', views.events,name="event"),
    path('group/', views.group,name="group"),
    path('capacity/', views.capacity,name="capacity"),
    path('eventview/<int:eid>', views.eventview,name="eventview"),
    path('editevent/<int:eid>', views.editevent,name="editevent"),
    path('finishevent/<int:eid>', views.finishevent,name="finishevent"),
    path('reopenevent/<int:eid>', views.reopenevent,name="reopen"),
    path('deleteevent/<int:eid>', views.deleteevent,name="deleteevent"),
    path('check_and_reassign_rooms/<int:event_id>/', views.check_and_reassign_rooms,name="check_and_reassign_rooms"),
    path('algo/', views.algo,name="algo"),
    path('result/<int:pk>/', views.result,name="result"),
    path('logout/', views.logout,name="logout"),
    path('status/<int:cid>', views.eventstatus,name="status"),
    path('mannual/<int:pk>', views.manuualy,name="manuualy"),
    path('viewcode/<int:pk>', views.view_code,name="view_code"),
    path('ajax/manual/', views.ajax_manual,name="ajax_manual"),
]
