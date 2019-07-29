from django.contrib import admin

# Register your models here.
from mall.forms import ProductAdminForm
from mall.models import Product, Classify, Tag
from utils.admin_actions import set_invalid, set_valid


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ 商品信息管理 """
    list_display = ('name', 'types', 'price', 'status', 'is_valid')
    # 修改分页大小
    list_per_page = 5
    list_filter = ('status', )
    # 排除掉一些字段，让其不能编辑，编辑界面不可见
    # exclude = ['remain_count']
    readonly_fields = ['remain_count']
    actions = [set_invalid, set_valid]
    # 自定义的表单
    form = ProductAdminForm

# 方式2 注册到后台管理
# admin.site.register(Product, ProductAdmin)


@admin.register(Classify)
class ClassifyAdmin(admin.ModelAdmin):
    """ 商品分类管理 """
    list_display = ['parent', 'name', 'code', 'is_valid']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ 商品分类管理 """
    list_display = ['name', 'code', 'is_valid']

