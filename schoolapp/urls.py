from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginORregister, name="loginORregister"),
    path('homepage/', views.homepage, name="homepage"),
    path('studentsrecord/', views.studentsrecord, name="studentsrecord"),
    path('teacherApi/', views.TeacherListCreate.as_view(), name="teacher-view-create"),
    path('teacher/', views.teacher, name="teacher"),
    path("edit_teacher/<int:id>/", views.edit_teacher, name="edit_teacher"),
    path("delete_teacher/<int:id>/", views.delete_teacher, name="delete_teacher"),
    path("edit_student/<int:id>/", views.edit_student, name="edit_student"),
    path("delete_student/<int:id>/", views.delete_student, name="delete_student"),
    path("student/", views.student, name="student"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    # path("loginORregister/", views.loginORregister, name="loginORregister"),
    path('studentApi/', views.StudentListCreate.as_view(), name="student-view-create"),
    
]
