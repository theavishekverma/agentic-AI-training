from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<str:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<str:student_id>/delete/', views.delete_student, name='delete_student'),
    path('students/<str:student_id>/quick-update/<str:field>/', views.quick_update, name='quick_update'),
]
