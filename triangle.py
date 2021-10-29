import glfw
from OpenGL.GL import *
import numpy as np
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

# tworzenie obecnego kontekstu- co kolwiek to znaczy
glfw.make_context_current(window)
#setowanie tła okna musi być poniżej kontekstu okna
vertices=np.array([-0.5,-0.5,0.0,0.5,-0.5,0.0,0.0,0.5,0.0], dtype=np.float32)
colors=np.array([1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,1.0],dtype=np.float32)
glEnableClientState(GL_VERTEX_ARRAY)
glEnableClientState(GL_COLOR_ARRAY)
glVertexPointer(3,GL_FLOAT,0,vertices)
glClearColor(100/255,170/255,30/255,1)
glColorPointer(3,GL_FLOAT,0,colors)
#główna pętla aplikacji
while not glfw.window_should_close(window):
    glfw.poll_events()
    #wstawianie koloru tła do głównej pętli
    glClear(GL_COLOR_BUFFER_BIT)

    ct = glfw.get_time()
    glLoadIdentity()
    glScale(abs(np.sin(ct)),abs(np.sin(ct)),1)
    glRotatef(np.sin(ct)*45,0,0,1)
    glTranslate(np.sin(ct),np.cos(ct),0)
    glDrawArrays(GL_TRIANGLES,0,3)
    glfw.swap_buffers(window)
#terminate glfw
print(glfw.get_time())
glfw.terminate()