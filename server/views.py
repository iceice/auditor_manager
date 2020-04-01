from django.http import JsonResponse
from .models import Student


# Create your views here.
def get_students(request):
    """获取所有学生信息"""
    try:
        obj_students = Student.objects.all().values()
        students = list(obj_students)
        return JsonResponse({'code': 1, 'data': students})
    except Exception as e:
        return JsonResponse({'code': 0, 'msg': "获取学生信息出现异常，具体错误：" + str(e)})
