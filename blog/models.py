from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.core.urlresolvers import reverse
from tagging.fields import TagField
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField('제목', max_length=50)
    slug = models.SlugField('슬러그', unique=True, allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField('요약', max_length=100, blank=True, help_text='simple description text.')
    content = models.TextField('내용')
    create_date = models.DateTimeField('생성 날짜', auto_now_add=True)
    modify_date = models.DateTimeField('수정 날짜', auto_now=True)
    tag = TagField('태그')
    owner = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table  = 'blog_posts'
        ordering  = ('-modify_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=(self.slug,))

    def get_previous_post(self):
        return self.get_previous_by_modify_date()

    def get_next_post(self):
        return self.get_next_by_modify_date()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

