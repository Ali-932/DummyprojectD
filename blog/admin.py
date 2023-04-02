from django.contrib import admin

from blog.models import articles, PermissionGroup, Writer

from guardian.admin import GuardedModelAdmin
from django.contrib.auth.models import Group, SubGroups
from .forms import  SubGroupForm, CustomGroupForm
from blog.models import articles


class ArticleAdmin(GuardedModelAdmin):
    list_display = ('title', 'slug', 'body')
    search_fields = ('title', 'body')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


admin.site.register(articles, ArticleAdmin)

class WriterAdmin(GuardedModelAdmin):
    list_display = ('name', 'slug', 'bio', 'date')
    search_fields = ('name', 'bio')
    ordering = ('-date',)
    date_hierarchy = 'date'

admin.site.register(Writer, WriterAdmin)
class GroupAdmin(admin.ModelAdmin):
    form = CustomGroupForm

    class Media:
        js = ('blog/dynamic_fields.js',)


admin.site.unregister(Group)
admin.site.register(PermissionGroup, GroupAdmin)


# class SubGroupAdmin(admin.ModelAdmin):
#     form = SubGroupForm
#
#
# admin.site.register(PermissionGroup, SubGroupAdmin)
