from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField('名称', max_length=50)
    status = models.PositiveIntegerField('状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    is_nav = models.BooleanField('是否为导航', default=False)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '分类'

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField('名称', max_length=10)
    status = models.PositiveIntegerField('状态', choices=STATUS_ITEMS, default=STATUS_NORMAL)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '标签'
    
class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField('标题', max_length=255)
    decs = models.CharField('摘要', max_length=1024, blank=True, null=True)
    content = models.TextField('正文', help_text='正文必须为markdown格式')
    status = models.PositiveIntegerField('状态', choices=STATUS_ITEMS, default=STATUS_NORMAL)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

