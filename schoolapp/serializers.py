from rest_framework import serializers
from . models import Teacher
from . models import Student

class TeachersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "gender", "phone_number", "email", "address" ]

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender", "phone_number", "email", "address" ]