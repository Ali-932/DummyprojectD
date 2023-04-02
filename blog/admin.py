from django.contrib import admin

from blog.models import articles

from guardian.admin import GuardedModelAdmin
from django.contrib.auth.models import Group, SubGroups
from .forms import CustomGroupAdminForm, SubGroupForm
from blog.models import articles

class ArticleAdmin(GuardedModelAdmin):
    list_display = ('title', 'slug', 'body')
    search_fields = ('title', 'body')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


admin.site.register(articles, ArticleAdmin)



class GroupAdmin(admin.ModelAdmin):
    form = CustomGroupAdminForm

    class Media:
        js = ('blog/dynamic_fields.js',)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

class SubGroupAdmin(admin.ModelAdmin):
    form = SubGroupForm

admin.site.register(SubGroups, SubGroupAdmin)

