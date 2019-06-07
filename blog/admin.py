from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . models import Post, Tag, Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time','owner')
    fields = ('name', 'status', 'is_nav', 'owner')

    #增加save_model方法，自动判断当前登陆的账号，用当前账号保存数据
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status', 'owner')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = []

    list_filter = ('category', )
    search_fields = ('title', 'category_name')

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True

    fields = (
        ('category', 'title'),
        'decs',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('admin:blog_post_change', args=(obj.id,)))
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)