
from minepi import Player, Skin
from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageOps
from os import listdir
from os.path import isfile, join
import json


def transparent_negative(img):
    rgb_im = img.convert('RGBA')
    for y in range(64):
        for x in range(64):
            r, g, b, t = rgb_im.getpixel((x, y))
            try: 
                if t != 0: rgb_im.putpixel((x, y), (255 - r, 255 - g, 255 - b, t))
            except: pass
    return rgb_im


def bw_mode(img):
    rgb_im = img.convert('RGBA')
    for y in range(64):
        for x in range(64):
            r, g, b, t = rgb_im.getpixel((x, y))
            try: 
                if t != 0: 
                    a = round((r + b + g) / 3)
                    rgb_im.putpixel((x, y), (a, a, a, t))
            except: pass
    return rgb_im
def average_colour(im):
    rgb_im = im.convert('RGBA')
    w, h = rgb_im.size
    r_a = 0
    g_a = 0
    b_a = 0
    num = 0
    for y in range(h):
        for x in range(w):
            r, g, b, t = rgb_im.getpixel((x, y))
            if t != 0:
                r_a += r
                g_a += g
                b_a += b
                num += 1

    return (255 - round(r_a / num), 255 - round(g_a / num), 255 - round(b_a / num))

def fill(img, colour):
    rgb_im = img.convert('RGBA')
    w, h = img.size
    r_c, g_c, b_c = colour
    for y in range(h):
        for x in range(w):
            r, g, b, t = rgb_im.getpixel((x, y))
            try: 
                if t != 0 and r == g == b: 
                    rgb_im.putpixel((x, y), (round((r / 255) * r_c), round((g / 255) * g_c), round((b / 255) * b_c), t))
            except: pass
    return rgb_im


def clear(img, pos, width):
    rgb_im = img.convert('RGBA')
    w, h = 16, width
    pos_x, pos_y = pos
    for y in range(h):
        for x in range(w):
            try: rgb_im.putpixel((x + pos_x, y + pos_y), (0, 0, 0, 0))
            except: pass
    return rgb_im

def paste_trans(img, shadow):
    rgb_im = img.convert('RGBA')
    shadow_im = shadow.convert('RGBA')
    
    w, h = rgb_im.size
    for y in range(h):
        for x in range(w):
            try: 
                r, g, b, t = rgb_im.getpixel((x, y))
                rs, gs, bs, ts = shadow_im.getpixel((x, y))
                if t != 0:
                    a = (r + b + g) // 3
                    
                    rgb_im.putpixel((x, y), (max(0, r - ts), max(0, g - ts), max(0, b - ts), t))
            except: pass
    return rgb_im

def crop(img, abs, slim, height):

    image = Image.open(img).convert("RGBA")
    if slim and (abs == 0 or abs == 2): image_o = image.crop((0, 0, 15, height+1))
    else: image_o = image.copy()

    if abs > 1:
        img_left = image_o.crop((0, 0, 8, height))
        img_right = image_o.crop((8, 0, 16, height))
        image_o = Image.new('RGBA', (16, height), (0, 0, 0, 0))
        image_o.paste(img_right, (0, 0), img_right)
        image_o.paste(img_left, (8 if not (slim and (abs == 0 or img == "res/pepes/pepe1.png" or abs == 2)) else 6, 0), img_left)

    return image_o
    
def to64(skin):
    new_img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    img = skin.copy()
    leg = img.crop((0, 16, 16, 32))
    arm = img.crop((40, 16, 64, 32))

    new_img.paste(leg, (16, 48), leg)
    new_img.paste(arm, (32, 48), arm)
    new_img.paste(img, (0, 0), img)

    leg_1 = img.crop((0, 20, 4, 32))
    leg_1 = ImageOps.mirror(leg_1)
    new_img.paste(leg_1, (24, 52), leg_1)

    leg_2 = img.crop((8, 20, 12, 32))
    leg_2 = ImageOps.mirror(leg_2)
    new_img.paste(leg_2, (16, 52), leg_2)

    leg_2 = img.crop((4, 20, 8, 32))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (20, 52), leg_2_m)

    leg_2 = img.crop((12, 20, 16, 32))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (28, 52), leg_2_m)

    leg_2 = img.crop((4, 16, 8, 20))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (20, 48), leg_2_m)

    leg_2 = img.crop((8, 16, 12, 20))
    leg_2_m = ImageOps.mirror(leg_2)
    new_img.paste(leg_2_m, (24, 48), leg_2_m)

    arm_1 = img.crop((40, 20, 44, 32))
    arm_1 = ImageOps.mirror(arm_1)
    new_img.paste(arm_1, (40, 52), arm_1)

    arm_1 = img.crop((48, 20, 52, 32))
    arm_1 = ImageOps.mirror(arm_1)
    new_img.paste(arm_1, (32, 52), arm_1)

    arm_1 = img.crop((44, 20, 48, 32))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (36, 52), arm_1_m)

    arm_1 = img.crop((52, 20, 56, 32))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (44, 52), arm_1_m)

    arm_1 = img.crop((44, 16, 48, 20))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (36, 48), arm_1_m)

    arm_1 = img.crop((48, 16, 52, 20))
    arm_1_m = ImageOps.mirror(arm_1)
    new_img.paste(arm_1_m, (40, 48), arm_1_m)

    return new_img

class Client:
    def __init__(self, chatId):
        self.chat_id = chatId
        self.slim = None
        self.slim_cust = 0
        self.mc_class = None
        self.skin_raw = None #img
        self.prewiew_id = 0
        self.info_id = 0
        self.delete_mess = False
        self.first_skin1 = None #img
        self.average_col = None
        self.pose = 0
        self.settings_mess = 0
        self.change_e = 0
        self.bandage = None
        self.error_msg = None
        self.wait_to_support = False
        self.wait_to_file = 0
        self.import_msg = -1
        self.waitToReview = -1
        self.ReviewMsg = None
        self.waitToBadge = False

        self.pos = 4
        self.colour = (-1, -1, -1)
        self.pepeImage = -1
        self.first_layer = 1
        self.overlay = True
        self.bw = False
        self.negative = False
        self.absolute_pos = 0
        self.delete_pix = True
        self.pepe_type = 0
        self.bandageRange = 8
        self.bandageHeight = 4
        self.view = False
    
        #leftArm leftLeg rightArm rightLeg
        self.x_f = [32, 16, 40, 0]
        self.y_f = [52, 52, 20, 20]
        self.x_o = [48, 0, 40, 0]
        self.y_o = [52, 52, 36, 36]

        self.pepes = ["pepe.png", "pepe1.png"]
        

        self.poses = [
            [0,  20, 10, 0], #vrll
            [0, -20,-10, 0], #vrrl
            [0, -20,-10, 0], #vrla
            [0,  20, 10, 0], #vrra
            [0,   0,  0, 90], #hrla
            [0,   0,  0, -90], #hrra
            [0,   0,  0, 20], #hrll
            [0,   0,  0, -20] #hrrl
        ]
        
        
    def reset(self):
        self.pos = (12 - self.bandageHeight) // 2
        self.colour = (-1, -1, -1)
        self.first_layer = 1
        self.overlay = True
        self.bw = False
        self.negative = False
        self.absolute_pos = 0
        self.delete_pix = True
        self.pepe_type = 0


    async def init_mc_f(self, usr_img):
        self.mc_class = Player(name="abc", raw_skin=usr_img)  # create a Player object by UUID
        await self.mc_class.initialize()
        self.skin_raw = usr_img
        self.first_skin1 = usr_img.copy()
        w, h = self.skin_raw.size
        if w != 64 or h != 64:
            self.skin_raw = self.first_skin1 = to64(self.skin_raw.copy())
        

    async def init_mc_n(self, name):
        done = 1
        self.mc_class = Player(name=name)  # create a Player object by UUID
        await self.mc_class.initialize()
        if self.mc_class._raw_skin == None: done = 0
        else:
            self.skin_raw = self.mc_class._raw_skin
            self.first_skin1 = self.mc_class._raw_skin.copy()

            w, h = self.skin_raw.size
            if w != 64 or h != 64:
                self.skin_raw = self.first_skin1 = to64(self.skin_raw.copy())

            for y_ch in range(3):
                for x_ch in range(3):
                    r, g, b, t = self.skin_raw.getpixel((x_ch, y_ch))
                    if t != 0:
                        done = 3
                        break
            
            if not bool(self.skin_raw.getpixel((46, 52))[3]) and not bool(self.skin_raw.getpixel((45, 52))[3]): done = 4

                    
            
        return done
        
    def exportJSON(self, chat):
        params = {
            "position": self.pos, 
            "firstLayer": self.first_layer, 
            "overlay": self.overlay, 
            "bw": self.bw, 
            "negative": self.negative, 
            "absolutePos": self.absolute_pos, 
            "layerDelete": self.delete_pix,
            "pepeType": self.pepe_type,
            "pepeImage": self.pepeImage
        }

        json_object = json.dumps(params, indent=9)
 
        with open(f"params{chat}.json", "w") as outfile:
            outfile.write(json_object)

    def importJSON(self, chat):
        with open(f'paramImported{chat}.json', 'r') as openfile:
            json_object = json.load(openfile)

        
        self.pos = int(json_object["position"])
        self.first_layer = int(json_object["firstLayer"])
        self.overlay = json_object["overlay"]
        self.bw = json_object["bw"]
        self.negative = json_object["negative"]
        self.absolute_pos = int(json_object["absolutePos"])
        self.delete_pix = json_object["layerDelete"]
        self.pepe_type = int(json_object["pepeType"])
        self.pepeImage = int(json_object["pepeImage"])
        

    async def prerender(self):
        if self.bw: self.skin_raw = bw_mode(self.skin_raw).copy()
        if self.negative: self.skin_raw = transparent_negative(self.skin_raw)
        
        mc_class = Player(name="abc", raw_skin=self.skin_raw)
        self.slim = self.mc_class.skin.is_slim
        await mc_class.initialize()
        
        await mc_class.skin.render_skin(hr=-45, vr=-20, ratio = 20, vrc = 15)
        img = mc_class.skin.skin
        self.average_col = average_colour(img.copy())
        
    async def rerender(self):

        self.skin_raw = self.first_skin1.copy()
        if self.colour != (-1, -1, -1):

            if self.delete_pix: self.skin_raw = clear(self.skin_raw.copy(), (self.x_o[self.absolute_pos], self.y_o[self.absolute_pos] + self.pos), self.bandageHeight)



            if self.pepeImage == -1: img = crop("res/pepes/" + str(self.pepes[self.pepe_type]), self.absolute_pos, self.slim, self.bandageHeight)
            else:img = crop(f"res/pepes/colored/{self.pepeImage}.png", self.absolute_pos, self.slim, self.bandageHeight)
            
            if self.pepeImage == -1: img = fill(img.copy(), self.colour)
            
            sl = self.slim and (self.absolute_pos == 0)
            if self.first_layer == 2: self.skin_raw.paste(img.crop((1, 0, 16, self.bandageHeight)) if sl else img, (self.x_f[self.absolute_pos], self.y_f[self.absolute_pos] + self.pos), img.crop((1, 0, 16, self.bandageHeight)) if sl else img)
            if self.overlay: self.skin_raw.paste(img.crop((1, 0, 16, self.bandageHeight)) if sl else img, (self.x_o[self.absolute_pos], self.y_o[self.absolute_pos] + self.pos), img.crop((1, 0, 16, self.bandageHeight)) if sl else img)

            
            bond = Image.new('RGBA', (16, self.bandageHeight), (0, 0, 0, 0))
            if self.first_layer == 1: 
                if self.pepeImage == -1: 
                    img_lining = Image.open("res/lining/custom.png")
                    img_lining = fill(img_lining.copy(), self.colour)
                else: img_lining = crop(f"res/lining/colored/{self.pepeImage}.png", self.absolute_pos, self.slim, self.bandageHeight)
                
                self.skin_raw.paste(img_lining.crop((2 if self.pepeImage == -1 else 1, 0, 16, self.bandageHeight)) if sl else img_lining, (self.x_f[self.absolute_pos], self.y_f[self.absolute_pos] + self.pos), img_lining.crop((2 if self.pepeImage == -1 else 1, 0, 16, self.bandageHeight)) if sl else img_lining)
                bond.paste(img_lining, (0, 0), img_lining)
            bond.paste(img, (0, 0), img)
            self.bandage = bond

            img.close()
        if self.bw: self.skin_raw = bw_mode(self.skin_raw).copy()

        r, g, b = self.average_col
        if self.negative: 
            self.skin_raw = transparent_negative(self.skin_raw)
            aver = 255 - r, 255 - g, 255 - b, 255
        else: aver = r, g, b, 255
        #render_image = paste_trans(self.skin_raw.copy(), Image.open("res/shadow.png"))
        #self.mc_class = Player(name="abc", raw_skin=self.skin_raw)
        #await self.mc_class.initialize()
        skin = Skin(self.skin_raw)

        if self.absolute_pos > 1:
            hr = 45 if not self.view else 135
        else:
            hr = -45 if not self.view else -135
        
        img = await skin.render_skin(hr=hr, 
                                    vr=-20, 
                                    ratio = 32, 
                                    vrc = 15, 
                                    vrll=self.poses[0][self.pose], 
                                    vrrl=self.poses[1][self.pose],
                                    vrla=self.poses[2][self.pose],
                                    vrra=self.poses[3][self.pose],
                                    hrla=self.poses[4][self.pose],
                                    hrra=self.poses[5][self.pose],
                                    hrll=self.poses[6][self.pose],
                                    hrrl=self.poses[7][self.pose],
                                    man_slim=self.slim_cust
                                    )
        
        img2 = await skin.render_skin(hr=hr, 
                                    vr=-20, 
                                    ratio = 32, 
                                    vrc = 15, 
                                    vrll=self.poses[0][self.pose], 
                                    vrrl=self.poses[1][self.pose],
                                    vrla=self.poses[2][self.pose],
                                    vrra=self.poses[3][self.pose],
                                    hrla=self.poses[4][self.pose],
                                    hrra=self.poses[5][self.pose],
                                    hrll=self.poses[6][self.pose],
                                    hrrl=self.poses[7][self.pose],
                                    man_slim=self.slim_cust,
                                    display_second_layer=False,
                                    display_cape=False
                                    )
        self.skin_raw.putpixel((0, 3), (255, 0, 0, 255))
        self.skin_raw.putpixel((3, 3), (0, 255, 0, 255))
        self.skin_raw.putpixel((3, 0), (0, 0, 255, 255))

        
        width, height = img.size
        width1, height1 = img2.size
        
        renderBack = Image.new(mode="RGBA", size=(height + 40, height + 40), color=aver)
        
        renderBack.paste(img2, (round((height1 + 40) / 2 - (width1 / 2)), 20), img2)
        renderBack.paste(img, (round((height + 40) / 2 - (width / 2)), 20), img)
        
        return renderBack
    
    


def find_client(list, chat_id):
    for num, i in enumerate(list):
        if i.chat_id == chat_id:
            return num
    return -1
