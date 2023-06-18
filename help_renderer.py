from PIL import Image, ImageFont, ImageDraw

def render(version):
    main = Image.open("res/help.png")

    fnt = ImageFont.truetype("res/font.ttf", 25)
    d = ImageDraw.Draw(main)

    d.text((180, 850), f"Версия: {version}", font=fnt, fill=(255, 255, 255))
    d.text((180, 880), "Created by AndcoolSystems", font=fnt, fill=(255, 255, 255))

    return main
