import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField

# Create your models here.
from django.db.models import F

from accounts.models import User
from system.models import ImageFile
from utils import constants


class Classify(models.Model):
    """ 商品的分类 """
    uid = models.UUIDField('商品ID', default=uuid.uuid4, editable=False)  # 随机生成的字符串 和系统、时间戳都有关系
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)  # 分类下面可能有自分类
    img = models.ImageField('分类主图', upload_to='classify')
    code = models.CharField('分类编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    desc = models.CharField('描述', max_length=64, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=False)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_classify'
        verbose_name = '商品分类'
        verbose_name_plural = '商品分类'
        ordering = ['-reorder']

    def __str__(self):
        return '{}.{}'.format(self.code, self.name)


class Tag(models.Model):
    """ 商品的标签 """
    uid = models.UUIDField('标签ID', default=uuid.uuid4, editable=False)  # 随机生成的字符串 和系统、时间戳都有关系
    img = models.ImageField('标签主图', upload_to='tags', null=True, blank=True)
    code = models.CharField('分类编码', max_length=32, null=True, blank=True)
    name = models.CharField('名称', max_length=12)
    reorder = models.SmallIntegerField('排序', default=0)
    is_valid = models.BooleanField('是否有效', default=False)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'mall_tag'
        verbose_name = '商品标签'
        verbose_name_plural = '商品标签'
        ordering = ['-reorder']

    def __str__(self):
        return '{}.{}'.format(self.code, self.name)


class Product(models.Model):
    """ 商品 """
    uid = models.UUIDField('商品ID', default=uuid.uuid4, editable=False)  # 随机生成的字符串 和系统、时间戳都有关系
    name = models.CharField('商品名称', max_length=128)
    desc = models.CharField('简单描述', max_length=128, null=True, blank=True)
    # content = models.TextField('商品描述',
    #                           null=True, blank=True)
    content = RichTextField('商品描述')

    types = models.SmallIntegerField('商品类型',
                                     choices=constants.PRODUCT_TYPES_CHOICES,
                                     default=constants.PRODUCT_TYPE_ACTUAL)

    price = models.IntegerField('兑换价格（积分兑换）')
    origin_price = models.FloatField('原价')
    image = models.ImageField('主要图片', upload_to='%Y%m/product')
    buy_link = models.CharField('购买链接', max_length=256, null=True, blank=True)
    reorder = models.SmallIntegerField('排序', default=0)
    status = models.SmallIntegerField('商品状态',
                                      choices=constants.PRODUCT_STATUS_CHOICES,
                                      default=constants.PRODUCT_STATUS_OFF)

    stock_count = models.IntegerField('库存', default=0)
    remain_count = models.IntegerField('剩余库存', default=0)
    view_count = models.IntegerField('浏览次数', default=0)
    score = models.FloatField('商品的评分', default=10.0)

    is_valid = models.BooleanField('商品是否有效', default=False)

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    tags = models.ManyToManyField(Tag, verbose_name='标签',
                                  related_name='tags',
                                  null=True, blank=True)
    classes = models.ManyToManyField(Classify, verbose_name='分类',
                                  related_name='classes',
                                  null=True, blank=True)
    banners = GenericRelation(ImageFile, verbose_name='banner_image',
                              related_query_name='banners')

    class Meta:
        db_table = 'mall_product'
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'
        ordering = ['-reorder']

    def update_store_count(self, count):
        """ 更改商品的库存信息 """
        self.remain_count = F('remain_count') - abs(count)
        self.save()
        self.refresh_from_db()

    def __str__(self):
        return self.name
