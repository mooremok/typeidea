from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from . models import Post, Tag, Category
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time','owner')
    fields = ('name', 'status', 'is_nav')

    #增加save_model方法，自动判断当前登陆的账号，用当前账号保存数据
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time', 'owner')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

#自定义Post过滤器，代码必须位于PostAdmin上方
class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    过滤器只展示当前帐户分类
    """
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
    
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_time', 'operator', 'owner')
    list_display_links = []

    list_filter = [CategoryOwnerFilter]
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