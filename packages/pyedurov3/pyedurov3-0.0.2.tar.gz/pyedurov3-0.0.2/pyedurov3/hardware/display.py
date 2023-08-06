import logging

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import adafruit_ssd1306

WIDTH = 128
HEIGHT = 64
BORDER = 1

TITLE_HEIGHT = 14
TITLE_BOX_WIDTH = 60

class Display(object):
    def __init__(self, oled_address=0x3C, loglevel="INFO"):

        print("Local UI init")
        self.loglevel = loglevel
        self.oled_available = False
        
        self._setup_oled(oled_address)

    def _setup_oled(self,address):
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=address)

        self.oled.fill(0)
        self.oled.show()
        
    def show_status(self,content):
        self._show_info("State",content)

    def show_error(self,error):
        image = Image.new("1", (self.oled.width, self.oled.height))

        self._clear_oled()
        self._draw_frame(image)
        self._draw_side_title(image,"Error " + error["id"])
        #print("text: "+error["short_description"])
        content = self._add_line_breaks(error["name"],10)
        #print("content: " + content)
        self._draw_text_box(image=image,text=content,bbox=(2,20,TITLE_BOX_WIDTH-2,HEIGHT-TITLE_HEIGHT-8))
        self._draw_icon(image,error["icon"])
        self.oled.image(image)
        self.oled.show()

    def show_error_details(self,error):
        self._show_info("Error Details",error["long_description"])

    def show_error_help(self,error):
        self._show_info("Error Help",error["help"])

    def show_shutdown_warning(self,remaining):
        image = Image.new("1", (self.oled.width, self.oled.height))

        self._clear_oled()
        self._draw_frame(image)
        self._draw_text_box(image,"Shutting down in \n"+ str(remaining) + "s",bbox=(2,2,120,60),alignment="center")
        self.oled.image(image)
        self.oled.show()

    def _show_info(self,title,content):
        image = Image.new("1", (self.oled.width, self.oled.height))

        self._clear_oled()
        self._draw_frame(image)
        self._draw_title(image,title)
        formatedContent = self._add_line_breaks(content,20)
        #print("content: " + content)
        self._draw_text_box(image=image,text=formatedContent,bbox=(2,20,WIDTH-4,HEIGHT-TITLE_HEIGHT-8))
        self.oled.image(image)
        self.oled.show()

    def _clear_oled(self):
        self.oled.fill(0)
        self.oled.show()
    
    def _draw_frame(self,image):
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a white background
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=255, fill=255)

        # Draw a smaller inner rectangle
        draw.rectangle(
            (BORDER, BORDER, self.oled.width - BORDER - 1, self.oled.height - BORDER - 1),
            outline=0,
            fill=0,
        )

    def _draw_title(self,image,title):
        draw = ImageDraw.Draw(image)

        # Load default font.
        font = ImageFont.load_default()

        (font_width, font_height) = font.getsize(title)

        draw.text(
            (self.oled.width // 2 - font_width // 2, 2),
            title,
            font=font,
            fill=255,
        )
        draw.line((0,TITLE_HEIGHT+1,self.oled.width,TITLE_HEIGHT+1),width=BORDER,fill=255)

    def _draw_side_title(self,image,title):
        draw = ImageDraw.Draw(image)

        draw.rectangle(
            (0, 0, TITLE_BOX_WIDTH, TITLE_HEIGHT),
            outline=255,
            fill=0,
        )

        # Load default font.
        font = ImageFont.load_default()

        draw.text(
            (5, 0),
            title,
            font=font,
            fill=255
        )

    def _find_last_space(self,line):
        charCount = len(line)
        i = charCount-1
        while i > 0:
            if line[i] == " ":
                return i
            i-=1
        
        return charCount

    def _add_line_breaks(self,text,charsPerLine = 12):
        newString = ""
        lineCount = 3
        restOfString = text

        for i in range(0,lineCount):
            #string has leading space
            if restOfString[0] == " ":
                restOfString = restOfString[1:]

            line = ""

            if len(restOfString) > charsPerLine:
                line = restOfString[0:charsPerLine]
                lastSpace = self._find_last_space(line)

                line = restOfString[0:lastSpace] + "\n"
                restOfString = restOfString[lastSpace:]
                #print("line: "+ line)
                #print("Rest: "+ restOfString)
                newString += line
            else:
                line=restOfString
                newString += line
                break

        return newString

    def _draw_text_box(self,image,text,bbox=(0,0,128,64),alignment="left"):

        textImage = Image.new("1", (bbox[2], bbox[3]))
        draw = ImageDraw.Draw(textImage)

        # Load default font.
        font = ImageFont.load_default()

        draw.multiline_text(
            (0,0),
            text,
            font=font,
            align=alignment,
            fill=255,
        )

        image.paste(textImage, (bbox[0],bbox[1]))

    def _draw_icon(self,image,filename):

        imagedir = Path(__file__).parent.parent.joinpath("images")
        defaultpath = imagedir.joinpath("error.png")
        imagepath = imagedir.joinpath(filename)

        #print(imagepath)
        
        if not imagepath.is_file():
            #print("File not available")
            imagepath = defaultpath

        with Image.open(imagepath) as image2:
            image2.load()
            image.paste(image2,(70,5))

        draw = ImageDraw.Draw(image)