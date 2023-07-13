#
#   task manager using pyxel as gui
#

import pyxel
import psutil

BASE_COLOR = 5
TEXT_COLOR = 0
CPU_CORES = psutil.cpu_count(logical=False)
CPU_CORES_LOG = psutil.cpu_count()

class DispGraph:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 100
        self.h = 40
        self.value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.update_time = 20
        self.last_time = 0

    def update(self, value):
        if (pyxel.frame_count - self.last_time) >= self.update_time:
            self.value.append(value)
            self.value.pop(0)
            self.last_time = pyxel.frame_count

    def draw(self):
        pyxel.rect(self.x+1, self.y+1, self.w, self.h, 1)
        pyxel.rect(self.x, self.y, self.w, self.h, BASE_COLOR)
        pyxel.rect(self.x+1, self.y+1, self.w-2, self.h-2, 7)
        pyxel.line(self.x+5, self.y+self.h-5, self.x+self.w-5, self.y+self.h-5, BASE_COLOR)
        #pyxel.text(self.x+5, self.y+5, str(self.value), TEXT_COLOR)
        self.drawgraph()

    def drawgraph(self):
        for i in range(len(self.value)):
            value_10 = int(self.value[i]//10)
            for j in range(value_10):
                pyxel.rect(self.x+6+i*9, self.y+self.h-8-j*3, 7, 1, BASE_COLOR)
            
class DispInfo:
    def __init__(self, title, x, y):
        self.title = title
        self.x = x
        self.y = y
        self.w = 45
        self.h = 16
        self.value = 0
        self.update_time = 20
        self.last_time = 0

    def update(self):
        pass
    def draw(self):
        pyxel.rect(self.x+1, self.y+1, self.w, self.h, 1)
        pyxel.rect(self.x, self.y, self.w, self.h, BASE_COLOR)
        pyxel.rect(self.x+1, self.y+1, self.w-2, self.h-2, 7)
        pyxel.text(self.x+5, self.y+5, self.title, TEXT_COLOR)
        pyxel.text(self.x+22, self.y+5, str(self.value), TEXT_COLOR)

class DispInfoCPU(DispInfo):
    def __init__(self, title, x, y):
        super().__init__(title, x, y)

    def update(self):
        if (pyxel.frame_count - self.last_time) >= self.update_time:
            self.value = psutil.cpu_percent(interval=1)
            self.last_time = pyxel.frame_count
    
    

class DispInfoMEM(DispInfo):
    def __init__(self, title, x, y):
        super().__init__(title, x, y)

    def update(self):
        if (pyxel.frame_count - self.last_time) >= self.update_time:
            self.value = psutil.virtual_memory().percent
            self.last_time = pyxel.frame_count

class App:
    def __init__(self):
        self.width = 160
        self.height = 120
        self.fps = 10
        self.app_title = "task_manager"
        pyxel.init(
            self.width, 
            self.height, 
            title=self.app_title, 
            display_scale=4, 
            fps=self.fps
        )
        self.cpu_obj = DispInfoCPU("cpu", 5, 20)
        self.mem_obj = DispInfoMEM("mem", 5, 70)
        self.cpu_graph = DispGraph(55, 20)
        self.mem_graph = DispGraph(55, 70)

        pyxel.run(self.update, self.draw)
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.cpu_obj.update()
        self.mem_obj.update()
        self.cpu_graph.update(self.cpu_obj.value)
        self.mem_graph.update(self.mem_obj.value)

    def draw(self):
        pyxel.cls(7)
        pyxel.text(10, 5, "status", TEXT_COLOR)
        pyxel.text(90, 5, "cpu cores:", TEXT_COLOR)
        pyxel.text(132, 5, str(CPU_CORES_LOG)+"("+str(CPU_CORES)+")", TEXT_COLOR)
        self.cpu_obj.draw()
        self.mem_obj.draw()
        self.cpu_graph.draw()
        self.mem_graph.draw()
        #pyxel.line(50, 27, 54, 27, 12)
        #pyxel.line(50, 77, 54, 77, 12)

App()
