from django.http import JsonResponse
from django.contrib.auth.models import Permission

def fetch_objects(request):
    permission_ids = request.GET.get('permission_ids', '').split(',')
    data = []

    if permission_ids:
        for permission_id in permission_ids:
            if not permission_id:
                continue
            permission = Permission.objects.get(pk=permission_id)
            model_class = permission.content_type.model_class()
            objects = model_class.objects.all()
            data.extend([{'id': obj.id, 'display': str(obj)} for obj in objects])

    # Removing duplicates
    data = list({frozenset(item.items()): item for item in data}.values())
    print(data)
    return JsonResponse(data, safe=False)
