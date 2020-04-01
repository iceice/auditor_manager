from django.db import models


# Create your models here.
# 学号，姓名，性别，出生日期，电话，邮箱，地址
class Student(models.Model):
    gender_choices = (('男', '男'), ('女', '女'))
    student_id = models.IntegerField(db_column="student_id", primary_key=True, null=False)
    name = models.CharField(db_column="name", max_length=100, null=False)
    gender = models.CharField(db_column="gender", max_length=32, choices=gender_choices)
    birthday = models.DateField(db_column="birthday", null=False)
    mobile = models.CharField(db_column="mobile", max_length=64)
    email = models.CharField(db_column="email", max_length=100)
    address = models.CharField(db_column="address", max_length=200)
    image = models.CharField(db_column="image", max_length=200, null=False)
    add_time = models.DateTimeField(auto_now_add=True)

    '''
    自定义表名
    '''
    class Meta:
        managed = True
        db_table = "Student"

    def __str__(self):
        return "学号: %s\t姓名: %s\t性别: %s" % (self.student_id, self.name, self.gender)
