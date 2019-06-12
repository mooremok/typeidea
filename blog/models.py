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
    
    def __str__(self):
        return self.name
    
    #获取分类函数
    @classmethod
    def get_navs(cls):
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        category = {
            'navs': nav_categories,
            'categories': normal_categories,
        }
        return category

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
    
    def __str__(self):
        return self.name
    
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
    #增加pv和uv，为sidebar提供封装支持
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title
    
    #封装最热文章，用only接口优化，只取title和id
    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(stauts=cls.STATUS_NORMAL).only('title', 'id').order_by('-pv')
    
    #视图部分函数抽象至model层
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, tag
    
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, category
    
    @classmethod
    def latest_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)      
