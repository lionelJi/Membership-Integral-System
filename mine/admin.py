from django.contrib import admin

# Register your models here.
from mine.models import Order, Cart, Comments


@ admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ 订单后台的管理 """
    list_display = ['sn', 'user', 'to_user', 'to_area']
    # 按照用户名和昵称搜索
    search_fields = ['user__username', 'user__nickname', 'to_user']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """  """
    list_display = ['name', 'user', 'price', 'img']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    """  """
    list_display = ['user', 'product', 'score', 'desc']
