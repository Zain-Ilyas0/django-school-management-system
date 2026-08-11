
from rest_framework import generics
from . models import Teacher
from . models import Student
from .serializers import TeachersSerializers
from .serializers import StudentSerializers
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

# Create your views here.



@login_required
def homepage(request):

    is_principal = request.user.groups.filter(
        name="Principal"
    ).exists()

    is_teacher = request.user.groups.filter(
        name="Teacher"
    ).exists()

    is_student = request.user.groups.filter(
        name="Student"
    ).exists()

    return render(request, "homepage.html", {
        "is_principal": is_principal,
        "is_teacher": is_teacher,
        "is_student": is_student,
    })







class TeacherListCreate(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeachersSerializers
    parser_classes = [FormParser, MultiPartParser]



@login_required
def teacher(request):

    if not request.user.groups.filter(name="Principal").exists():
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        Teacher.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            address=address,
            gender=gender
        )

    teachers = Teacher.objects.all()

    return render(request, "teacher.html", {
        "teachers": teachers
    })



@login_required
def edit_teacher(request, id):

    if not request.user.groups.filter(name="Principal").exists():
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    teacher = get_object_or_404(Teacher, id=id)

    if request.method == "POST":
        teacher.first_name = request.POST.get("first_name")
        teacher.last_name = request.POST.get("last_name")
        teacher.gender = request.POST.get("gender")
        teacher.phone_number = request.POST.get("phone_number")
        teacher.email = request.POST.get("email")
        teacher.address = request.POST.get("address")

        teacher.save()

        return redirect("teacher")

    teachers = Teacher.objects.all()

    return render(request, "teacher.html", {
        "teachers": teachers,
        "edit_teacher": teacher
    })

@login_required
def delete_teacher(request, id):

    if not request.user.groups.filter(name="Principal").exists():
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    teacher = get_object_or_404(Teacher, id=id)

    teacher.delete()

    return redirect("teacher")




class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializers
    parser_classes = [FormParser, MultiPartParser]


@login_required
def student(request):

    allowed = request.user.groups.filter(
        name__in=["Principal", "Teacher"]
    ).exists()

    if not allowed:
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            address=address,
            gender=gender
        )

    students = Student.objects.all()

    return render(request, "student.html", {
        "students": students
    })




@login_required
def edit_student(request, id):

    allowed = request.user.groups.filter(
        name__in=["Principal", "Teacher"]
    ).exists()

    if not allowed:
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.first_name = request.POST.get("first_name")
        student.last_name = request.POST.get("last_name")
        student.gender = request.POST.get("gender")
        student.phone_number = request.POST.get("phone_number")
        student.email = request.POST.get("email")
        student.address = request.POST.get("address")

        student.save()

        return redirect("student")

    students = Student.objects.all()

    return render(request, "student.html", {
        "students": students,
        "edit_student": student
    })

@login_required
def delete_student(request, id):

    allowed = request.user.groups.filter(
        name__in=["Principal", "Teacher"]
    ).exists()

    if not allowed:
        return HttpResponseForbidden(
            "You are not allowed to access this page."
        )

    student = get_object_or_404(Student, id=id)

    student.delete()

    return redirect("student")




# def studentsrecord(request):
#     students = Student.objects.all()

#     return render(request, "studentsrecord.html", {
#         "students": students
#     })

from django.db.models import Q

@login_required
def studentsrecord(request):
    query = request.GET.get("search", "")

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(gender__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )

    return render(request, "studentsrecord.html", {
        "students": students,
        "query": query
    })






def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            return redirect("homepage")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, "login.html")


def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists."
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("login")

    return render(request, "register.html")



def loginORregister(request):
    return render(request, "loginORregister.html")