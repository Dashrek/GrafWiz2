import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
import numpy as np
from TextureLoader import load_texture,load_texture_crop, sierra2
from matplotlib import pyplot as plt
from ObjLoader import ObjLoader
from shaders import *
import datetime
import os
import winsound
from scipy.io import wavfile
import multiprocessing
from playsound import playsound
from scipy.io import wavfile
# glfw callback functions
import math
class menu_muzyki:
    def __init__(self):
        self.lista=[]
        for i in os.listdir():
            if "wav" in i.split("."):
                self.lista+=[i]
    def projection(self):
        for j,i in enumerate(self.lista):
            print(j,i)
        print("wybierz utwór")
    def wybor(self):
        a=int(input())
        if a>len(self.lista):
            return ""
        print("Wybrano",self.lista[a])
        return self.lista[a]


def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    matryce["projekcji"] = pyrr.matrix44.create_perspective_projection_matrix(45, width / (height+0.00001)+0.00001, 0.1, 100)
    glUniformMatrix4fv(layouty["proj_loc"], 1, GL_FALSE, matryce["projekcji"])


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

# load here the 3d meshes
obiekty = {}
for i in ["zegar","sekundnik","minutnik","godzinnik","lewy","prawy","g1","g2","g3","g4","ekran"]:
    obiekty[i+"_indices"], obiekty[i+"_buffer"] = ObjLoader.load_model(i+".obj")

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# VAO and VBO
VAO = glGenVertexArrays(11)
VBO = glGenBuffers(11)
plansze={"zegar_array":VAO[0],
         "sekundnik_array":VAO[1],
         "minutnik_array":VAO[2],
         "godzinnik_array":VAO[3],
         "lewy_array":VAO[4],
         "ekran_array":VAO[5],
         "g1_array":VAO[6],
         "g2_array":VAO[7],
         "g3_array":VAO[8],
         "g4_array":VAO[9],
         "prawy_array":VAO[10],
         "zegar_buffers":VBO[0],
         "sekundnik_buffers":VAO[1],
         "minutnik_buffers":VBO[2],
         "godzinnik_buffers":VBO[3],
         "lewy_buffers": VBO[4],
         "ekran_buffers":VBO[5],
         "g1_buffers": VBO[6],
         "g2_buffers": VBO[7],
         "g3_buffers": VBO[8],
         "g4_buffers": VBO[9],
         "prawy_buffers": VBO[10],
         }
textures = glGenTextures(11)
textury={}
for j,i in enumerate(["zegar","sekundnik","minutnik","godzinnik","lewy","prawy","g1","g2","g3","g4","ekran"]):
    textury[i+".png"]=textures[j]
for i in ["zegar","sekundnik","minutnik","godzinnik","lewy","prawy","g1","g2","g3","g4","ekran"]:
    #VAO
    glBindVertexArray(plansze[i+"_array"])
    glBindBuffer(GL_ARRAY_BUFFER, plansze[i+"_array"])
    glBufferData(GL_ARRAY_BUFFER, obiekty[i+"_buffer"].nbytes, obiekty[i+"_buffer"], GL_STATIC_DRAW)
    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, obiekty[i+"_buffer"].itemsize * 8, ctypes.c_void_p(0))
    # textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, obiekty[i+"_buffer"].itemsize * 8, ctypes.c_void_p(12))
    # normals
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, obiekty[i+"_buffer"].itemsize * 8, ctypes.c_void_p(20))
    if i not in ["g1","g2","g3","g4","ekran"]:
        load_texture(i + ".png", textury[i + ".png"])
    else:
        load_texture("liczby.png", textury[i + ".png"])
glUseProgram(shader)
glClearColor(0.2,0.1,0.2,1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
matryce={"projekcji":pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100),
         "zegar":pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -2])),
         }
for i in ("sekundnik","minutnik","godzinnik","lewy","prawy","g1","g2","g3","g4","ekran"):
    matryce[i]=matryce["zegar"]

# eye, target, up
view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -1]))
layouty={
    "model_loc":glGetUniformLocation(shader, "model"),
    "proj_loc":glGetUniformLocation(shader, "projection"),
    "view_loc":glGetUniformLocation(shader, "view"),
    "light_loc":glGetUniformLocation(shader, "light")
}

import multiprocessing
glUniformMatrix4fv(layouty["proj_loc"], 1, GL_FALSE, matryce["projekcji"])
glUniformMatrix4fv(layouty["view_loc"], 1, GL_FALSE, view)
The=menu_muzyki()
The.projection()
sciezki=(lambda a: [a.split(".")[0]+".png", a])(The.wybor())
#t=plt.imread(sciezki[0])
#try:
#    os.remove("tymczasowy.png")
#except:
#    print("Nie było pliku tymczasowego!")
#plt.imsave("tymczasowy.png",sierra2(t))
samplerate, data1=wavfile.read(sciezki[1])
data2={
    "lewy":data1[:,0],
    "prawy":data1[:,1]
}
winsound.PlaySound(sciezki[1], winsound.SND_ASYNC | winsound.SND_ALIAS )
czas1=glfw.get_time()
# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    godzina=datetime.datetime.now()
    czas={"sekundnik":godzina.second,
          "minutnik":godzina.minute+godzina.second/60,
          "godzinnik":godzina.hour%12*5+godzina.minute/12}
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_y = pyrr.Matrix44.from_y_rotation(0.2 )#* glfw.get_time())
    glUniformMatrix4fv(layouty["light_loc"], 1, GL_FALSE, pyrr.Matrix44.from_y_rotation(0.2*glfw.get_time() ))
    model = pyrr.matrix44.multiply(rot_y, matryce["zegar"])

    # draw the chibi character
    glBindVertexArray(plansze["zegar_array"])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(layouty["model_loc"], 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(obiekty["zegar_indices"]))
    # glDrawElements(GL_TRIANGLES, len(obiekty["zegar_indices"]), GL_UNSIGNED_INT, None)
    for i in ["sekundnik","minutnik","godzinnik"]:
        rot_y = pyrr.Matrix44.from_z_rotation(2*np.pi/360*6 * czas[i]) @ pyrr.Matrix44.from_y_rotation(0.2 )
        model = pyrr.matrix44.multiply(rot_y, matryce[i])
        # draw the monkey head
        glBindVertexArray(plansze[i+"_array"])
        glBindTexture(GL_TEXTURE_2D, textury[i+".png"])
        glUniformMatrix4fv(layouty["model_loc"], 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(obiekty[i+"_buffer"]))
    for i in ["lewy","prawy"]:
        rot_y = pyrr.Matrix44.from_y_rotation(0.2 )
        model = pyrr.matrix44.multiply(rot_y, matryce[i])
        load_texture_crop(i+".png",textury[i+".png"],int(np.abs(data2[i][int((glfw.get_time()-czas1)*samplerate)])/32758*200),0,200,200)
        glBindVertexArray(plansze[i+"_array"])
        glBindTexture(GL_TEXTURE_2D, textury[i+".png"])
        glUniformMatrix4fv(layouty["model_loc"], 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(obiekty[i+"_buffer"]))
    rot_y = pyrr.Matrix44.from_y_rotation(0.2)
    model = pyrr.matrix44.multiply(rot_y, matryce[i])
    load_texture(sciezki[0], textury["ekran.png"])
    #load_texture("tymczasowy.png", textury["ekran.png"])
    glBindVertexArray(plansze["ekran_array"])
    glBindTexture(GL_TEXTURE_2D, textury["ekran.png"])
    glUniformMatrix4fv(layouty["model_loc"], 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(obiekty["ekran_buffer"]))
    for i in ["g1","g2","g3","g4"]:
        rot_y = pyrr.Matrix44.from_y_rotation(0.2 )
        model = pyrr.matrix44.multiply(rot_y, matryce[i])
        load_texture_crop("liczby.png",textury[i+".png"],0,200*int((str(godzina.hour).zfill(2)[0] if i=="g1" else( str(godzina.hour).zfill(2)[1] if i=="g2" else (str(godzina.minute).zfill(2)[0]if i=="g3" else str(godzina.minute).zfill(2)[1]))))//1,200,200)
        glBindVertexArray(plansze[i+"_array"])
        glBindTexture(GL_TEXTURE_2D, textury[i+".png"])
        glUniformMatrix4fv(layouty["model_loc"], 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(obiekty[i+"_buffer"]))
    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()