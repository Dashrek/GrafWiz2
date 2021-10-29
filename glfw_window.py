import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader,compileProgram
import numpy as np
from shaderstory import *
def window_resize(window, width, height):
    glViewport(0,0,width,height)
#inicjalizacja biblioteki
if not glfw.init():
    raise Exception("glfw can not be initialized")
#tworzenie nowego okna
window=glfw.create_window(1280,720, "Zegar holenderski",None,None) # pierwszy none może zmienić się w fullscreen, drugi "for share resources"

#sprawdzanie czy okno powstało
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created")
#ustawianie pozycji okna
glfw.set_window_pos(window, 400,200)
glfw.set_window_size_callback(window,window_resize)

# tworzenie obecnego kontekstu- co kolwiek to znaczy
glfw.make_context_current(window)
#setowanie tła okna musi być poniżej kontekstu okna
vertices=np.array([-0.5,-0.5,0.0, 1.0,0.0,0.0,
                   0.5,-0.5,0.0,  0.0,1.0,0.0,
                   -0.5,0.5,0.0, 0.0,0.0,1.0,
                   0.5, 0.5, 0.0, 1.0, 1.0, 1.0,
                   0.0,0.75,0.0,1.0,1.0,0.0], dtype=np.float32)
indicies=np.array([0,1,2,
          1,2,3, 2,3,4], np.uint32)
#shader ustawianie
shader= compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))
VBO=glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER,VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes,vertices,GL_STATIC_DRAW)

EBO=glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicies.nbytes,indicies,GL_STATIC_DRAW)

#position=glGetAttribLocation(shader,"a_position")
glEnableVertexAttribArray(0)#position
glVertexAttribPointer(0, 3, GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(0))

#color=glGetAttribLocation(shader,"a_color")
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT,GL_FALSE,24,ctypes.c_void_p(12))

glUseProgram(shader)
glClearColor(0.2,0.1,0.2,1)
#główna pętla aplikacji
while not glfw.window_should_close(window):
    glfw.poll_events()
    #wstawianie koloru tła do głównej pętli
    glClear(GL_COLOR_BUFFER_BIT)
    #glDrawArrays(GL_TRIANGLE_STRIP,0,4)
    glDrawElements(GL_TRIANGLES, len(indicies), GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)
#terminate glfw
print(glfw.get_time())
glfw.terminate()