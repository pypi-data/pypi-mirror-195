import re
import base64
from io import BytesIO
from PIL import Image as Image_, ImageFont, ImageDraw


class Image:
    def __init__(self, data):
        if isinstance(data, str):
            if 'data:image' in data:
                data = self.decode_base64(data)
                self.instance = Image_.open(BytesIO(data))
                return
            self.instance = Image_.open(data)
        elif isinstance(data, bytes):
            self.instance = Image_.open(BytesIO(data))
        else:
            pass

    @staticmethod
    def decode_base64(base64_str):
        """解码base64为图像数据"""
        base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
        return base64.b64decode(base64_data)

    def watermark(self, text, font_size=36):
        image = self.instance.copy().convert('RGB')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('arial.ttf', font_size)
        x = 0
        y = image.size[1] - font_size
        draw.text((x, y), text, font=font, fill=(255, 0, 0))
        rst = Image(1)
        rst.instance = image
        return rst
    
    def trim(self):
        box = self.instance.getbbox()
        rst = Image(1)
        rst.instance = self.instance.crop(box)
        return rst

    @property
    def size(self):
        return self.instance.size

    @property
    def bytes(self):
        with BytesIO() as output:
            self.instance.save(output, format="PNG")
            return output.getvalue()


