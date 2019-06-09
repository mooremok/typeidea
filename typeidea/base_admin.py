from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1.用以自动补全文章、分类、标签、侧边栏、友链等model的owner字段
    2.用以过滤当前用户的queryset数据
    """

    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)