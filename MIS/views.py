from datetime import datetime

from django.shortcuts import render

from accounts.models import User
from mall.models import Product
from system.models import Slider, News
from utils import constants


def index(request):
    """ 首页 """
    # 查询轮播图
    slider_list = Slider.objects.filter(types=constants.SLIDER_TYPES_INDEX)

    # 首页的新闻
    now_time = datetime.now()
    # 过滤出置顶的，有效的，在时间范围内的
    news_list = News.objects.filter(types=constants.NEWS_TYPE_NEW,
                                    is_top=True,
                                    is_valid=True,
                                    start_time__lte=now_time,
                                    end_time__gte=now_time)

    # 精选推荐
    recommend_list = Product.objects.filter(
        status = constants.PRODUCT_STATUS_SELL,
        is_valid = True,
        tags__code = 'recommend'
    )

    # 至宝专区
    ancient_list = Product.objects.filter(
        status = constants.PRODUCT_STATUS_SELL,
        is_valid = True,
        tags__code = 'Ancient'
    )

    # 不朽专区
    arcana_list = Product.objects.filter(
        status = constants.PRODUCT_STATUS_SELL,
        is_valid = True,
        tags__code = 'Arcana'
    )

    # # 从session中获取用户ID
    # user_id = request.session[constants.LOGIN_SESSION_ID]
    # # 查询当前登陆的用户
    # user = User.objects.get(pk=user_id)
    return render(request, 'index.html', {
        'slider_list': slider_list,
        'news_list': news_list,
        'recommend_list': recommend_list,
        'ancient_list': ancient_list,
        'arcana_list': arcana_list,
        # 'user': user,
    })
