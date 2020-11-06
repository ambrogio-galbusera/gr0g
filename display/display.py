import ST7735
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from fonts.ttf import RobotoMedium as UserFont


class Display:

    def __init__ (self) :
        print("[DISP] Initialized\n")

        # Create ST7735 LCD display class
        self.st7735 = ST7735.ST7735(
            port=0,
            cs=1,
            dc=9,
            backlight=12,
            rotation=270,
            spi_speed_hz=10000000
        )

        # Initialize display
        self.st7735.begin()

        self.WIDTH = self.st7735.width
        self.HEIGHT = self.st7735.height

        # Set up canvas and font
        self.img = Image.new('RGBA', (self.WIDTH, self.HEIGHT), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        self.font_size_small = 10
        self.font_size_large = 20
        self.font = ImageFont.truetype(UserFont, self.font_size_large)
        self.smallfont = ImageFont.truetype(UserFont, self.font_size_small)

    def drawInit (self) :
        print("[DISP] Draw init\n")
        self.draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), (255, 255, 255))

    def update (self) :
        print("[DISP] Update\n")
        self.st7735.display(self.img)

    def icon (self,pos,aicon) :
        self.img.paste(aicon, pos, mask=aicon)

    def image (self,imageName) :
        self.img = Image.open(imageName)
        self.draw = ImageDraw.Draw(self.img)

    def text (self,pos,text) :
        print("[DISP] Text ({}) {}\n".format(pos,text))
        self.draw.text(pos,text,font=self.font, fill=(0, 0, 0))

    def overlay_text(self,pos, text, font_large, align_right=False, rectangle=False):
        font = self.smallfont
        if font_large:
            font = self.font

        w, h = font.getsize(text)
        if align_right:
            x, y = pos
            x -= w
            position = (x, y)
        if rectangle:
            x += 1
            y += 1
            pos = (x, y)
            border = 1
            rect = (x - border, y, x + w, y + h + border)
            rect_img = Image.new('RGBA', (self.WIDTH, self.HEIGHT), color=(0, 0, 0, 0))
            rect_draw = ImageDraw.Draw(rect_img)
            rect_draw.rectangle(rect, (255, 255, 255))
            rect_draw.text(pos, text, font=font, fill=(0, 0, 0, 0))
            self.img = Image.alpha_composite(self.img, rect_img)
        else:
            self.draw.text(pos, text, font=font, fill=(255, 255, 255))


