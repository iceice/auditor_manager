from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from .models import Student
import json
import uuid
import hashlib
import os


# Create your views here.
def get_students(request):
    """
    获取所有学生信息
    """
    try:
        obj_students = Student.objects.all().values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "获取学生信息出现异常，具体错误：" + str(e)})


def query_students(request):
    """
    查询学生的信息
    """
    data = json.loads(request.body.decode('utf-8'))
    query_str = data['inputstr']
    try:
        obj_students = Student.objects.filter(
            Q(student_id__icontains=query_str) | Q(name__icontains=query_str)
            | Q(gender__icontains=query_str) | Q(mobile__icontains=query_str)
            | Q(email__icontains=query_str)
            | Q(address__icontains=query_str)).values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "查询学生信息出现异常，具体错误：" + str(e)})


def check_studentID(request):
    """
    检查学生ID是否存在
    """
    data = json.loads(request.body.decode('utf-8'))
    query_str = data['student_id']
    try:
        obj_students = Student.objects.filter(student_id=query_str)
        if (obj_students.count() == 0):
            return JsonResponse({'code': 1, 'existed': False})
        else:
            return JsonResponse({'code': 1, 'existed': True})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "校验学号失败，具体错误：" + str(e)})


def add_student(request):
    """
    添加一个学生
    """
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_students = Student(student_id=data['student_id'],
                               name=data['name'],
                               gender=data['gender'],
                               birthday=data['birthday'],
                               mobile=data['mobile'],
                               email=data['email'],
                               address=data['address'],
                               image=data['image'])
        obj_students.save()
        obj_students = Student.objects.all().values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "添加到数据库失败，具体错误：" + str(e)})


def update_student(request):
    """
    修改学生信息
    """
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_students = Student.objects.get(student_id=data['student_id'])
        # 判断之前的图片是否需要删除
        if obj_students.image:
            file_path = os.path.join(settings.MEDIA_ROOT, obj_students.image)
            if os.path.exists(file_path):
                os.remove(file_path)
        obj_students.name = data['name']
        obj_students.gender = data['gender']
        obj_students.birthday = data['birthday']
        obj_students.mobile = data['mobile']
        obj_students.email = data['email']
        obj_students.address = data['address']
        obj_students.image = data['image']
        obj_students.save()
        obj_students = Student.objects.all().values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "修改保存到数据库失败，具体错误：" + str(e)})


def delete_student(request):
    """
    删除一个学生
    """
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj_students = Student.objects.get(student_id=data['student_id'])
        # 删除图片信息
        file_path = os.path.join(settings.MEDIA_ROOT, obj_students.image)
        if os.path.exists(file_path):
            os.remove(file_path)
        obj_students.delete()
        obj_students = Student.objects.all().values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "删除学生信息写入数据库失败，具体错误：" + str(e)})


def delete_students(request):
    """
    批量删除学生信息
    """
    data = json.loads(request.body.decode('utf-8'))
    try:
        for one in data['student']:
            obj_student = Student.objects.get(student_id=one['student_id'])
            # 删除图片信息
            file_path = os.path.join(settings.MEDIA_ROOT, obj_student.image)
            if os.path.exists(file_path):
                os.remove(file_path)
            obj_student.delete()
        obj_students = Student.objects.all().values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({
            'code': 0,
            'msg': "批量删除学生信息写入数据库失败，具体错误：" + str(e)
        })


def upload(request):
    """
    接收上传的文件
    """
    rev_file = request.FILES.get('avatar')
    if not rev_file:
        return JsonResponse({'code': 0, 'msg': "图片不存在！"})
    # 生成唯一的名字
    new_name = get_random_str()
    file_path = os.path.join(settings.MEDIA_ROOT,
                             new_name + os.path.splitext(rev_file.name)[1])
    try:
        f = open(file_path, 'wb')
        # 如果文件比较大，分多次写入
        for i in rev_file.chunks():
            f.write(i)
        f.close()
        return JsonResponse({
            'code':
            1,
            'name':
            new_name + os.path.splitext(rev_file.name)[1]
        })
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "具体错误：" + str(e)})


def get_random_str():
    uuid_val = uuid.uuid4()
    uuid_str = str(uuid_val).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(uuid_str)
    return md5.hexdigest()
