
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/completelist', views.completelist, name='completeList'),
    path('tasks/create', views.create, name='create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.task_complete, name='task_complete'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),

]
