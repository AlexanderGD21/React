from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course-list'),
    path('<int:pk>/', views.course_detail, name='course-detail'),
    path('<int:pk>/quiz/', views.course_quiz, name='course-quiz'),
    path('<int:pk>/submit/', views.submit_quiz, name='submit-quiz'),
    path('questions/', views.question_list, name='question-list'),
]
