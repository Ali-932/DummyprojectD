from django.contrib.contenttypes.models import ContentType
from guardian.models import GroupObjectPermission
from django.contrib.auth.models import  Permission
from guardian.shortcuts import assign_perm, remove_perm


from django.contrib.contenttypes.models import ContentType
from guardian.models import GroupObjectPermission
from django.contrib.auth.models import Permission
from guardian.shortcuts import assign_perm, remove_perm


def assign_permissions_and_objects_to_group(group, permissions, objects, is_editing=False):
    if is_editing:
        GroupObjectPermission.objects.filter(group=group).delete()

        for perm in Permission.objects.all():
            remove_perm(f"{perm.content_type.app_label}.{perm.codename}", group)

    # for different content types
    content_type_object_map = {}
    for obj in objects:
        content_type = ContentType.objects.get_for_model(obj)
        if content_type not in content_type_object_map:
            content_type_object_map[content_type] = []
        content_type_object_map[content_type].append(obj)

    for perm in permissions:
        objs = content_type_object_map.get(perm.content_type, [])
        for obj in objs:
            assign_perm(perm.codename, group, obj=obj)
    # for parent group
    for child_group in group.tn_children.all():
        GroupObjectPermission.objects.filter(group=child_group).delete()

        child_group_permissions = Permission.objects.filter(group=child_group, content_type__in=content_type_object_map.keys())

        for perm in child_group_permissions:
            objs = content_type_object_map.get(perm.content_type, [])
            for obj in objs:
                assign_perm(perm.codename, child_group, obj=obj)
    # for child group
    if parent_group := group.tn_parent:
        parent_group_permissions = Permission.objects.filter(group=parent_group, content_type__in=content_type_object_map.keys())

        for perm in parent_group_permissions:
            GroupObjectPermission.objects.filter(group=parent_group, permission=perm).delete()

            objs = content_type_object_map.get(perm.content_type, [])
            for obj in objs:
                assign_perm(perm.codename, parent_group, obj=obj)
