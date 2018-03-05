from django.db import models


# university 테이블(클래스) 정의
class University(models.Model):
    university_id = models.AutoField(primary_key=True)
    university_name = models.CharField(max_length=50)

    # university 레코드(객체) 메소드 정의
    def __str__(self):
        return self.university_name


# college 테이블(클래스) 정의
class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=50)
    university = models.ForeignKey('University', on_delete=models.CASCADE, null=True)

    # college 레코드(객체) 메소드 정의
    def __str__(self):
        return self.college_name


# department 테이블(클래스) 정의
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50)
    college = models.ForeignKey('College', on_delete=models.CASCADE, null=True)

    # department 레코드(객체) 메소드 정의
    def __str__(self):
        return self.department_name


# course 테이블(클래스) 정의
class Course(models.Model):
    course_id = models.CharField(max_length=60, primary_key=True)
    course_number = models.CharField(max_length=50)
    course_semester = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)
    course_time = models.CharField(max_length=50)
    course_professor = models.CharField(max_length=50)
    course_credit = models.IntegerField()
    course_note = models.CharField(max_length=50)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)

    # course 레코드(객체) 메소드 정의
    def __str__(self):
        return self.course_name