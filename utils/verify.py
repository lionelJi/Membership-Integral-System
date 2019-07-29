"""
Verify Code module
1. 准备素材
    字体(ttf)，文字内容，颜色，干扰线
2.

"""
import io
import os
import random

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.http import HttpResponse


class VerifyCode(object):
    """ 验证码类 """

    def __init__(self, dj_request):
        # 验证码图片尺寸
        self.dj_request = dj_request
        self.code_len = 4  # length of verify code
        self.img_width = 100
        self.img_height = 30

        self.session_key = 'verify_code'

    def gen_code(self):
        code = self._get_vcode()
        # 把验证码存在session中
        self.dj_request.session[self.session_key] = code
        # 准备随机元素
        font_color = ['black', 'brown', 'red', 'darkblue', 'darkred', 'green', 'darkmagenta', 'cyan']
        # 随机背景色
        bg_color = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        # 字体路径
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Lato-BlackItalic.ttf')
        # 创建图片
        im = Image.new('RGB', (self.img_width, self.img_height), bg_color)
        draw = ImageDraw.Draw(im)

        # 画随机条数的干扰线
        for i in range(random.randrange(1, int(self.code_len/2)+1)):
            line_color = random.choice(font_color)
            point = (
                random.randrange(0, self.img_width * 0.2),
                random.randrange(0, self.img_height),
                random.randrange(self.img_width * 0.8, self.img_width),
                random.randrange(0, self.img_height),
            )  # 点的位置
            width = random.randint(1,4)  # 线条的宽度
            draw.line(point, fill=line_color, width=width)

        # 画验证码
        for index, char in enumerate(code):
            code_color = random.choice(font_color)
            font_size = random.randint(15, 25)
            font = ImageFont.truetype(font_path, font_size)
            point = (
                index * self.img_width / self.code_len,
                random.randrange(0, self.img_height/3)
            )
            draw.text(point, char, font=font, fill=code_color)

        buf = io.BytesIO()
        im.save(buf, 'gif')
        return HttpResponse(buf.getvalue(), 'image/gif')

    def _get_vcode(self):
        """ 生成验证码 """
        random_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        code_list = random.sample(list(random_str), self.code_len)
        code = ''.join(code_list)
        return code

    def validate_code(self, code):
        """ 验证码是否正确 """
        # 转变大小写
        code = str(code).lower()
        vcode = self.dj_request.session.get(self.session_key, '')
        return vcode.lower() == code


if __name__ == '__main__':
    client = VerifyCode(None)
    client.gen_code()
