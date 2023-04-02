from django.http import JsonResponse
from django.contrib.auth.models import Permission

def fetch_objects(request):
    if permission_id := request.GET.get('permission_id'):
        permission = Permission.objects.get(pk=permission_id)
        model_class = permission.content_type.model_class()
        objects = model_class.objects.all()
        data = [{'id': obj.id, 'display': str(obj)} for obj in objects]
    else:
        data = []
    return JsonResponse(data, safe=False)
