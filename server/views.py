from django.http import JsonResponse
from django.db.models import Q
from .models import Student
import json


# Create your views here.
def get_students(request):
    """获取所有学生信息"""
    try:
        obj_students = Student.objects.all().values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "获取学生信息出现异常，具体错误：" + str(e)})


def query_students(request):
    """查询学生的信息"""
    data = json.loads(request.body.decode('utf-8'))
    query_str = data['inputstr']
    try:
        obj_students = Student.objects.filter(
            Q(student_id__icontains=query_str) |
            Q(name__icontains=query_str) |
            Q(gender__icontains=query_str) |
            Q(mobile__icontains=query_str) |
            Q(email__icontains=query_str) |
            Q(address__icontains=query_str)
        ).values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "查询学生信息出现异常，具体错误：" + str(e)})
