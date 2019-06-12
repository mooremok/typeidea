from django.db import models
from django.contrib.auth.models import User
#from django.shortcuts import render
from django.template.loader import render_to_string
# Create your models here.

class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    title = models.CharField('标题', max_length=50)
    href = models.URLField('链接') #默认长度为200
    status = models.PositiveIntegerField('状态', choices=STATUS_ITEMS, default=STATUS_NORMAL)
    weight = models.PositiveIntegerField('权重', choices=zip(range(1, 6), range(1, 6)), default=1, help_text='数值越高排名越前')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '友情链接'
    
    def __str__(self):
        return self.title

class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 2
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )
    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    )
    title = models.CharField('标题', max_length=50)
    display_type = models.PositiveIntegerField('展示类型', choices=SIDE_TYPE, default=1)
    content = models.CharField('内容', help_text='如果设置的不是HTML类型，可为空', blank=True, max_length=500)
    status = models.PositiveIntegerField('状态', choices=STATUS_ITEMS, default=STATUS_SHOW)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'

    def __str__(self):
        return self.title
    
    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)     

    @property
    def content_html(self):
        """直接渲染模板"""
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.latest_posts(),
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.hot_posts(),
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL),
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)
        return result

