# Pillow to read every pixel from a image
#from email.mime import image
import platform
from PIL import Image
# Json for img to json convertion and vice versa
import json
import sys
import random

# Recommended Maximum: 76x76

class color():
    r = '\033[1;0m'
    def rgb(r=0,g=255,b=50):
        return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'
    def brgb(r=0,g=255,b=50):
        return '\033[48;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

class itj():
    # Print an Image
    def img_to_text(scling = 1, shrink = 1, img = 'img.png', bw = False, rc = 0, gc = 1, bc = 2, ac = 3, brgb = color.brgb, rgb = color.rgb, r = color.r):
        scling = int(scling)
        shrink = int(shrink)
        img = Image.open(img)
        img = img.convert('RGB')
        scaling = img.size
        i = 0
        while i+shrink+1 <= scaling[1]:
            i2 = 0
            pval = ''
            while i2+shrink <= scaling[0]:
                val = img.getpixel((i2,i))
                try:
                    val2 = img["pix"][i+1][i2]
                except:
                    try:
                        val2 = img["pix"][i][i2]
                    except:
                        val2 = (0,0,0,0)
                if bw:
                    rgb = int((val[0]+val[1]+val[2])/3)
                    rgb2 = int((val2[0]+val2[1]+val2[2])/3)
                    pval = pval+brgb(rgb2,rgb2,rgb2)+rgb(rgb,rgb,rgb)+'▀'*scling
                else:
                    pval = pval+brgb(val2[0], val2[1], val2[2])+rgb(val[0], val[1], val[2])+'▀'*scling
                i2 += shrink
            i += 1+shrink
            print(pval+r)
        img.close()

    # Convert an image to json
    def img_to_json(scling = 1, shrink = 1, img = 'img.png', bw = False, rc = 0, gc = 1, bc = 2, ac = 3, rgb = color.rgb, r = color.r):
        jo = {
            "name": "lol",
            "w": 0,
            "h": 0,
            "pix": []
        }
        jol = json.loads(json.dumps(jo))
        sp = '/'
        if 'Windows' in platform.system():
            sp = '\\'
        jol["name"] = img.split(sp)[len(img.split(sp))-1]
        scling = int(scling)
        shrink = int(shrink)
        img = Image.open(img)
        img = img.convert('RGBA')
        scaling = img.size
        jol["w"] = int(scaling[0]/shrink)
        jol["h"] = int(scaling[1]/shrink)
        i = 0
        while i+shrink <= scaling[1]:
            i2 = 0
            pval = []
            while i2+shrink <= scaling[0]:
                val = img.getpixel((i2,i))
                if bw:
                    rgb1 = int((val[0]+val[1]+val[2])/3)
                    pval.append([rgb1,rgb1,rgb1,val[ac]])
                else:
                    pval.append([val[rc],val[gc],val[bc],val[ac]])
                i2 += shrink
            i += shrink
            jol["pix"].append(pval)
        img.close()
        return json.dumps(jol, indent=4)
    
    # Print the image from json
    def json_to_text(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[],[]]}', bw = False, rc = 0, gc = 1, bc = 2, ac = 3, brgb = color.brgb, rgb = color.rgb, r = color.r):
        img = json.loads(json2)
        scling = int(scling)
        shrink = int(shrink)
        scaling = (img["w"]*scling,img["h"]*scling)
        i = 0
        while i+shrink <= scaling[1]:
            i2 = 0
            pval = ''
            while i2+shrink <= scaling[0]:
                val = img["pix"][i][i2]
                try:
                    val2 = img["pix"][i+1][i2]
                except:
                    try:
                        val2 = img["pix"][i][i2]
                    except:
                        val2 = (0,0,0,0)
                if bw:
                    rgb1 = int((val[0]+val[1]+val[2])/3)
                    rgb2 = int((val2[0]+val2[1]+val2[2])/3)
                    pval = pval+brgb(rgb2,rgb2,rgb2)+rgb(rgb1,rgb1,rgb1)+'▀'*scling
                else:
                    pval = pval+brgb(val2[0], val2[1], val2[2])+rgb(val[0], val[1], val[2])+'▀'*scling
                i2 += shrink
            i += shrink+1
            print(pval+r)

    # Modify with the image as json
    def manage_json(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[0,0,0,0],[]]}', bw = False, rc = 0, gc = 1, bc = 2, ac = 3, rgb = color.rgb, r = color.r):
        jo = {
            "name": "lol",
            "w": 0,
            "h": 0,
            "pix": []
        }
        jol = json.loads(json.dumps(jo))
        img = json.loads(json2)
        scling = int(scling)
        shrink = int(shrink)
        jol["name"] = img["name"]
        jol["w"] = int(img["w"]/shrink)*scling
        jol["h"] = int(img["h"]/shrink)*scling
        scaling = (img["w"],img["h"])
        i = 0
        while i+shrink <= scaling[1]:
            i2 = 0
            pval = []
            while i2+shrink <= scaling[0]:
                val = img["pix"][i][i2]
                for i3 in range(0,scling):
                    if bw:
                        rgb1 = int((val[0]+val[1]+val[2])/3)
                        pval.append([rgb1,rgb1,rgb1,val[ac]])
                    else:
                        pval.append([val[rc],val[gc],val[bc],val[ac]])
                i2 += shrink
            i += shrink
            for i3 in range(0,scling):
                jol["pix"].append(pval)
        return json.dumps(jol, indent=4)
    
    # Convert Json to an Image
    def json_to_image(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[0,0,0,0],[]]}', bw = False, rc = 0, gc = 1, bc = 2, ac = 3, output = 'img.png', rgb = color.rgb, r = color.r):
        js = json.loads(json2)
        img = Image.new(mode = 'RGB', size = (js["w"]*scling,js['h']*scling))
        scaling = (js["w"],js["h"])
        i = 0
        while i+shrink <= scaling[1]:
            for if3 in range(0,scling):
                i2 = 0
                while i2+shrink <= scaling[0]:
                    val = js["pix"][i][i2]
                    for if4 in range(0,scling):
                        if bw:
                            rgb1 = int((val[0]+val[1]+val[2])/3)
                            img.putpixel( (int(i2*scling+if4),int(i*scling+if3)) , (rgb1,rgb1,rgb1, val[ac]) )
                        else:
                            img.putpixel( (int(i2*scling+if4),int(i*scling+if3)) , (val[rc],val[gc],val[bc], val[ac]) )
                    i2 += shrink
            i += shrink
        img.save(output)
        img.close()

class tests():
    # generate a random image
    def generateRandomImage(WIDTH = 76, HEIGHT = 76, BW = False, NAME = "Garbage"):
        jo = {
            "name": "lol",
            "w": WIDTH,
            "h": HEIGHT,
            "pix": []
        }

        # Generate nonsense
        for h in range(HEIGHT):
            jo["pix"].append([])
            for w in range(WIDTH):
                rand_r = random.randrange(0,255)
                rand_g = random.randrange(0,255)
                rand_b = random.randrange(0,255)
                jo["pix"][h].append([rand_r,rand_g,rand_b, 1])

        return json.dumps(jo, indent=4)