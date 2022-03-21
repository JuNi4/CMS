from PIL import Image
import platform
import json

class color():
    r = '\033[1;0m'
    def rgb(r=0,g=255,b=50):
        return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'
def img_to_text(scling = 1, shrink = 1, img = 'img.png', rgb = color.rgb, r = color.r):
    scling = int(scling)
    shrink = int(shrink)
    img = Image.open(img)
    img = img.convert('RGB')
    scaling = img.size
    i = 0
    while i+shrink <= scaling[1]:
        i2 = 0
        pval = ''
        while i2+shrink <= scaling[0]:
            val = img.getpixel((i2,i))
            pval = pval+rgb(val[0], val[1], val[2])+'██'*scling
            i2 += shrink
        i += shrink
        print(pval+r)
def img_to_json(scling = 1, shrink = 1, img = 'img.png', rgb = color.rgb, r = color.r):
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
    img = img.convert('RGB')
    scaling = img.size
    jol["w"] = int(scaling[0]/shrink)
    jol["h"] = int(scaling[1]/shrink)
    i = 0
    while i+shrink <= scaling[1]:
        i2 = 0
        pval = []
        while i2+shrink <= scaling[0]:
            val = img.getpixel((i2,i))
            pval.append([val[0],val[1],val[2]])
            i2 += shrink
        i += shrink
        jol["pix"].append(pval)
    return json.dumps(jol, indent=4)

def json_to_text(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[],[]]}', rgb = color.rgb, r = color.r):
    img = json.loads(json2)
    scling = int(scling)
    shrink = int(shrink)
    scaling = (img["w"],img["h"])
    i = 0
    while i+shrink <= scaling[1]:
        i2 = 0
        pval = ''
        while i2+shrink <= scaling[0]:
            val = img["pix"][i][i2]
            pval = pval+rgb(val[0], val[1], val[2])+'██'*scling
            i2 += shrink
        i += shrink
        print(pval+r)

def manage_json(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[0,0,0],[]]}', rgb = color.rgb, r = color.r):
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
    jol["w"] = int(img["w"]/shrink)
    jol["h"] = int(img["h"]/shrink)
    scaling = (img["w"],img["h"])
    i = 0
    while i+shrink <= scaling[1]:
        i2 = 0
        pval = []
        while i2+shrink <= scaling[0]:
            try:
                val = img["pix"][i][i2]
            except:
                val = img["pix"][i2][i]
            pval.append([val[0],val[1],val[2]])
            i2 += shrink
        i += shrink
        jol["pix"].append(pval)
    return json.dumps(jol, indent=4)