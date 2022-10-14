# Pillow to read every pixel from a image
#from email.mime import image
import platform
from PIL import Image
# Json for img to json convertion and vice versa
import json
import sys

# Empfolenes Maximum: 38x38

class itj():
        
    class color():
        r = '\033[1;0m'
        def rgb(r=0,g=255,b=50):
            return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'
        def brgb(r=0,g=255,b=50):
            return '\033[48;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

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

    def manage_json(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[0,0,0],[]]}', bw = False, rc = 0, gc = 1, bc = 2, ac = 3, rgb = color.rgb, r = color.r):
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
    
    def json_to_image(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[0,0,0],[]]}', bw = False, rc = 0, gc = 1, bc = 2, ac = 3, output = 'img.png', rgb = color.rgb, r = color.r):
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