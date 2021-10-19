import glfw
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
#główna pętla aplikacji
while not glfw.window_should_close(window):
    glfw.poll_events()
    glfw.swap_buffers(window)
#terminate glfw
glfw.terminate()