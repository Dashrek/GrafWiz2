from OpenGL.GL import glBindTexture, glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, \
    GL_TEXTURE_WRAP_T, GL_REPEAT, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR,\
    glTexImage2D, GL_RGBA, GL_UNSIGNED_BYTE
from PIL import Image
from matplotlib import cm
import math
from HSVANDRGB import *
from matplotlib import pyplot as plt
import numpy as np

# for use with GLFW
def load_texture(path, texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    # Set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image
    image = Image.open(path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture

def load_texture_crop(path, texture,y1=0,x1=0,x=2000,y=2000):
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    image = Image.open(path)
    image=image.crop((x1,y1,x+x1,y+y1))
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture


def sierra2(obraz_wej,prog=0.5):
    ka=np.max(obraz_wej)
    print(ka)
    wartosc=0
    if ka>1: wartosc=255
    elif ka<=1: wartosc=1.0
    prog=prog*wartosc
    print(prog,ka)
    e_tab=np.zeros(obraz_wej.shape)
    shapes=obraz_wej.shape
    obraz_wyj=np.zeros(obraz_wej.shape)
    for k in range(e_tab.shape[2]):

        for j in range(e_tab.shape[0]):
            if j%100==0:
                print(j)
            for i in range(e_tab.shape[1]):
                e=0
                if prog>(obraz_wej[j,i,k]+e_tab[j,i,k]):
                    obraz_wyj[j,i,k]=0
                    e=obraz_wej[j,i,k]+e_tab[j,i,k]

                else:
                    obraz_wyj[j, i, k] = wartosc
                    e=obraz_wej[j,i,k]+e_tab[j,i,k]-wartosc
                for z in [(i-2,j+1,1/16),(i-1,j+1,2/16),(i,j+1,3/16),(i+1,j,4/16),(i+2,j,3/16),(i+1,j+1,2/16),(i+2,j+1,1/16)]:
                    if z[0]>=0 and z[0]<=shapes[1]-1 and z[1]>=0 and z[1]<=shapes[0]-1:
                        e_tab[z[1],z[0],k]=e_tab[z[1],z[0],k]+e*z[2]
    return obraz_wyj


