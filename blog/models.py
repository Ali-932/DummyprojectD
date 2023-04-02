from django.db import models


class Writer(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    bio = models.TextField()
    date = models.DateTimeField()


    def __str__(self):
        return self.name


class articles(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_article_writer', 'Can view writer'),
            ('view_articles', 'Can view articles'),
            ('sign_articles', 'Can sign articles'),
        )
        get_latest_by = 'created_at'


