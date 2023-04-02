from itertools import chain

from django import forms
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from guardian.models import GroupObjectPermission
from guardian.shortcuts import assign_perm, get_objects_for_group, get_perms_for_model

from django.db.models import Q
from django import forms
from django.contrib.auth.models import Group, Permission
from guardian.shortcuts import assign_perm, remove_perm


class CustomGroupAdminForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        label='Select permissions for the new group'
    )
    selected_objects = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        label='Select objects for the selected permission'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_editing = self.instance.pk is not None

        if permission_ids := self.data.getlist('permissions'):
            permission_id = self.data.get('permissions')
            selected_permission = Permission.objects.get(pk=permission_id)
            model_class = selected_permission.content_type.model_class()
            self.fields['selected_objects'].queryset = model_class.objects.all()
        else:
            self.fields['selected_objects'].queryset = Permission.objects.filter(Q(pk=None))

    def save(self, commit=True):
        group = super().save(commit=False)
        group.save()

        # If editing, delete all previous permissions
        if self.is_editing:
            # Remove all object permissions for the group
            GroupObjectPermission.objects.filter(group=group).delete()

            # Remove all model-level permissions for the group
            for perm in self._get_all_global_permissions():
                remove_perm(f"{perm.content_type.app_label}.{perm.codename}", group)

        permissions = self.cleaned_data.get('permissions')

        if selected_objects := self.cleaned_data.get('selected_objects'):
            for perm in permissions:
                assign_perm(perm.codename, group, obj=selected_objects)

        self.save_m2m()
        return group

    def _get_all_global_permissions(self):
        return Permission.objects.all()


class SubGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        label='Select permissions for the sub group')

    selected_group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label='Select an existing group'
    )


    def save(self, commit=True):
        group = super().save(commit=False)
        selected_group = self.cleaned_data['selected_group']
        permissions = self.cleaned_data['permissions']
        objs = self.get_all_objects_for_group(selected_group) if selected_group else []
        group.is_template = False
        group.save()

        print(objs)

        # Assigning permissions to the new group for the unique objects
        for obj in objs:
            for perm in permissions:
                assign_perm(perm, group, obj=obj)

        self.save_m2m()
        return group

    def get_all_objects_for_group(self, group):
        # Get all GroupObjectPermissions for the group
        group_perms = GroupObjectPermission.objects.filter(group=group)

        # Fetch objects for each GroupObjectPermission
        objs_with_perms = []
        for group_perm in group_perms:
            content_type = group_perm.content_type
            obj = content_type.get_object_for_this_type(pk=group_perm.object_pk)
            objs_with_perms.append(obj)

        return list(set(objs_with_perms))

