from django.urls import path
from core import views

urlpatterns = [
    path('',views.HomepageView.as_view(),name='home'),
    path('create_todo/',views.CreateTodo.as_view(),name='new'),
    path('login/',views.LoginRegisterView.as_view(),name='login'),
    path('detail/<int:pk>/',views.TodoDetailView.as_view(),name='details'),
    path('upcoming/',views.Upcoming.as_view(),name='upcoming'),
    path('edit/<int:pk>/',views.EditTodo.as_view(),name='edit'),
    path('delete/<int:pk>/',views.delete_todo,name='delete'),
    path('logout/',views.logout_user,name='logout')
]