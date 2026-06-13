from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<str:student_id>/edit/', views.edit_student, name='edit_student'),
    path('students/<str:student_id>/delete/', views.delete_student, name='delete_student'),
    path('students/<str:student_id>/quick-update/<str:field>/', views.quick_update, name='quick_update'),
    # AI endpoints (Claude)
    path('ai/chat/', views.ai_chat, name='ai_chat'),
    path('ai/insights/', views.ai_insights, name='ai_insights'),
    path('ai/report/<str:student_id>/', views.ai_student_report, name='ai_student_report'),
    # AI endpoints (Gemini)
    path('gemini/chat/', views.gemini_chat, name='gemini_chat'),
    path('gemini/summary/', views.gemini_smart_summary, name='gemini_smart_summary'),
    path('gemini/report/<str:student_id>/', views.gemini_student_report, name='gemini_student_report'),
]
