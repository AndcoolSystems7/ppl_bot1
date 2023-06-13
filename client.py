from minepi import Player
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from os import listdir
from os.path import isfile, join


def transparent_negative(img):
    rgb_im = img.convert('RGBA')
    for y in range(64):
        for x in range(64):
            r, g, b, t = rgb_im.getpixel((x, y))
            try: 
                if t != 0: rgb_im.putpixel((x, y), (255 - r, 255 - g, 255 - b, t))
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
                if t != 0: 
                    rgb_im.putpixel((x, y), (round((r / 255) * r_c), round((g / 255) * g_c), round((b / 255) * b_c), t))
            except: pass
    return rgb_im


def clear(img, pos):
    rgb_im = img.convert('RGBA')
    w, h = 16, 4
    pos_x, pos_y = pos
    for y in range(h):
        for x in range(w):
            try: rgb_im.putpixel((x + pos_x, y + pos_y), (0, 0, 0, 0))
            except: pass
    return rgb_im

def crop(image, abs, slim):
    new_img = Image.new('RGBA', (16, 4), (0, 0, 0, 0))
    img = Image.open(image).convert("RGBA")
    if abs > 1: 
        if abs == 2 and slim:
            img_less = img.crop((0, 0, 1, 5))
            img_h = img.crop((1, 0, 6, 4))
            new_img.paste(img_less, (13, 0), img_less)
            new_img.paste(img_h, (0, 0), img_h)
        else:
            img_less = img.crop((0, 0, 1, 5))
            
            img_h = img.crop((1, 0, 6, 4))
            new_img.paste(img_less, (15, 0), img_less)
            new_img.paste(img_h, (0, 0), img_h)
    else:
        new_img.paste(img, (7, 0), img)
    return new_img

class Client:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.slim = None
        self.pos = 4
        self.colour = 0
        self.wait_to_file = 0
        self.mc_class = None
        self.skin_raw = None #img
        self.prewiew_id = 0
        self.info_id = 0
        self.colour_list = [(0, 0, 0), (176, 30, 30), (85, 163, 64), (61, 58, 201), (250, 213, 30), (0, 0, 0)]
        self.delete_mess = False
        self.first_skin1 = None #img
        self.average_col = None
        self.first_layer = 1
        self.overlay = True
        self.bw = False
        self.negative = False
        self.pose = 0
        self.bondg_color = (0, 0, 0)
        self.absolute_pos = 0
        self.settings_mess = 0
        self.change_e = 0
        #leftArm leftLeg rightArm rightLeg
        self.x_f = [32, 16, 40, 0]
        self.y_f = [52, 52, 20, 20]
        self.x_o = [48, 0, 40, 0]
        self.y_o = [52, 52, 36, 36]

        self.pepes = [f for f in listdir("res/pepes") if isfile(join("res/pepes", f))]
        self.pepe_type = 0

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
        
        
        
    async def init_mc_f(self, usr_img):
        
        
        self.mc_class = Player(name="abc", raw_skin=usr_img)  # create a Player object by UUID
        await self.mc_class.initialize()
        self.skin_raw = usr_img
        self.first_skin1 = usr_img.copy()
        
        

    async def init_mc_n(self, name):
        done = True
        self.mc_class = Player(name=name)  # create a Player object by UUID
        await self.mc_class.initialize()
        if self.mc_class._raw_skin == None: done = False
        else:
            self.skin_raw = self.mc_class._raw_skin
            self.first_skin1 = self.mc_class._raw_skin.copy()
        return done
        

    async def prerender(self):
        if self.bw: self.skin_raw = self.skin_raw.convert('LA').copy()
        if self.negative: self.skin_raw = transparent_negative(self.skin_raw)
        
        mc_class = Player(name="abc", raw_skin=self.skin_raw)  # create a Player object by UUID
        #self.skin_raw = self.first_skin1
        self.slim = self.mc_class.skin.is_slim
        await mc_class.initialize()
        
        await mc_class.skin.render_skin(hr=-45, vr=-20, ratio = 20, vrc = 15)
        img = mc_class.skin.skin
        self.average_col = average_colour(img.copy())
        
        
    
    async def rerender(self):
        self.skin_raw = self.first_skin1.copy()
        if self.colour != 0:
            self.skin_raw = clear(self.skin_raw.copy(), (self.x_o[self.absolute_pos], self.y_o[self.absolute_pos] + self.pos))

            img = crop("res/pepes/" + str(self.pepes[self.pepe_type]), self.absolute_pos, self.slim)
            if self.absolute_pos > 1: 
                if self.absolute_pos == 2 and self.slim:
                    img_pod = Image.open("res/custom_right_arm.png")
                else:
                    img_pod = Image.open("res/custom_right.png")
            else:
                img_pod = Image.open("res/custom.png")
            
            self.colour_list[5] = self.bondg_color
            img_pod = fill(img_pod.copy(), self.colour_list[self.colour])

            img.paste(img_pod, (0, 0), img_pod)
            sl = self.slim and (self.absolute_pos == 0)
            if self.first_layer == 2: self.skin_raw.paste(img.crop((1, 0, 16, 4)) if sl else img, (self.x_f[self.absolute_pos], self.y_f[self.absolute_pos] + self.pos), img.crop((1, 0, 16, 4)) if sl else img)
            if self.overlay: self.skin_raw.paste(img.crop((1, 0, 16, 4)) if sl else img, (self.x_o[self.absolute_pos], self.y_o[self.absolute_pos] + self.pos), img.crop((1, 0, 16, 4)) if sl else img)

            
            
            if self.first_layer == 1: 
                img_lining = Image.open("res/lining/custom.png")
                img_lining = fill(img_lining.copy(), self.colour_list[self.colour])
                self.skin_raw.paste(img_lining.crop((1, 0, 16, 4)) if sl else img_lining, (self.x_f[self.absolute_pos], self.y_f[self.absolute_pos] + self.pos), img_lining.crop((1, 0, 16, 4)) if sl else img_lining)

            
            img.close()
        if self.bw: 
            self.skin_raw = self.skin_raw.convert('LA').copy()
            enhancer = ImageEnhance.Contrast(self.skin_raw)
            factor = 1.5 
            self.skin_raw = enhancer.enhance(factor)

        if self.negative: 
            self.skin_raw = transparent_negative(self.skin_raw)
            r, g, b = self.average_col
            average_col = 255 - r, 255 - g, 255 - b
        else: average_col = self.average_col
        self.mc_class = Player(name="abc", raw_skin=self.skin_raw)  # create a Player object by UUID
        await self.mc_class.initialize()
        
        await self.mc_class.skin.render_skin(hr=45 if self.absolute_pos > 1 else -45, 
                                             vr=-20, 
                                             ratio = 20, 
                                             vrc = 15, 
                                             vrll=self.poses[0][self.pose], 
                                             vrrl=self.poses[1][self.pose],
                                             vrla=self.poses[2][self.pose],
                                             vrra=self.poses[3][self.pose],
                                             hrla=self.poses[4][self.pose],
                                             hrra=self.poses[5][self.pose],
                                             hrll=self.poses[6][self.pose],
                                             hrrl=self.poses[7][self.pose]
                                             )
        img = self.mc_class.skin.skin
        
        new_img = None

        width, height = img.size
        new_img = Image.new('RGB', (height + 20, height + 20), average_col)
        new_img.paste(img, (round((height + 20) / 2) - round
                            (width / 2), 10), img)
        return new_img
    
    
    
def find_client(list, chat_id):
    if list == []: 
        list = [Client(chat_id)]
        id = 0
    else:
        finded = False
        for add in range(len(list)):
            if list[add].chat_id == chat_id:
                finded = True
                id = add
                break
        if not finded: 
            list.append(Client(chat_id))
            id = len(list) - 1
    return id
