"""
Provides the simulator graphics implementation
public:
graphics
"""

import time
from PySide import QtCore, QtGui, QtOpenGL

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "PyMorphous",
                            "PyOpenGL must be installed to run PyMorphous.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)
    
import Image

import pymorphous.implementation.simulator.constants

class _SimulatorWindow(QtGui.QWidget):
    def __init__(self, cloud, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.cloud = cloud
        self.glWidget = _SimulatorGLWidget(cloud)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(self.tr(cloud.window_title))

_color_id_counter = 0

def _get_color_id(lst):
    return lst[0] + lst[1]*128 + lst[2]*128*128

class _SimulatorUniqueColor(object):
    def __init__(self):
        global _color_id_counter
        self.value = _color_id_counter
        _color_id_counter += 1
        
    @property
    def red(self):
        return self.value % 128
    
    @property
    def green(self):
        return (self.value/128) % 128
    
    @property
    def blue(self):
        return self.value/(128*128) % 128
        
class _SimulatorGLWidget(QtOpenGL.QGLWidget):
    
    def __init__(self, cloud, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        
        self.cloud = cloud
        
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.selected_device = None
        
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.myupdate)
        timer.start(1000.0/self.cloud.desired_fps)
        self.last_time = time.time()
        self.start_time = time.time()
        self.recording = self.cloud.auto_record
        self.frameno = 0
        
        self.color_dict = {}
        for d in self.cloud.devices:
            d.color_id = _SimulatorUniqueColor()
            self.color_dict[str(d.color_id.value)] = d
    
    def __del__(self):
        self.makeCurrent()
        glDeleteLists(self.listSimpleBody, 1)
        glDeleteLists(self.listSelect, 1)
        glDeleteLists(self.listRadio, 1)
        glDeleteLists(self.listSelectedDevice, 1)
        for i in range(3):
            glDeleteLists(self.listLeds[i], 1)

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glutInit()
        
        self.listSimpleBody = glGenLists(1);
        if not self.listSimpleBody:
            raise SystemError("""Unable to generate display list using glGenLists""")
        glNewList(self.listSimpleBody, GL_COMPILE)
        glutWireSphere(*self.cloud.settings.graphics.simple_body_dim)
        glEndList()
        
        self.listSelect = glGenLists(1);
        if not self.listSelect:
            raise SystemError("""Unable to generate display list using glGenLists""")
        glNewList(self.listSelect, GL_COMPILE)
        glutSolidSphere(*self.cloud.settings.graphics.select_dim)
        glEndList()
        
        self.listSelectedDevice = glGenLists(1);
        if not self.listSelectedDevice:
            raise SystemError("""Unable to generate display list using glGenLists""")
        glNewList(self.listSelectedDevice, GL_COMPILE)
        glutSolidSphere(*self.cloud.settings.graphics.selected_device_dim)
        glEndList()
        
        self.listRadio = glGenLists(1);
        if not self.listRadio:
            raise SystemError("""Unable to generate display list using glGenLists""")
        glNewList(self.listRadio, GL_COMPILE)
        glutSolidSphere(0.8*4, 8, 8) # TODO
        glEndList()
        
        self.listBlendLed = glGenLists(1);
        if not self.listBlendLed:
            raise SystemError("""Unable to generate display list using glGenLists""")
        glNewList(self.listBlendLed, GL_COMPILE)
        glutSolidSphere(0.8, 8, 8) # TODO
        glEndList()
        
        self.listSenses = []
        for i in range(3):
            self.listSenses += [glGenLists(1)]
            if not self.listSenses[i]:
                raise SystemError("""Unable to generate display list using glGenLists""")
            glNewList(self.listSenses[i], GL_COMPILE)
            glutSolidSphere(*self.cloud.settings.graphics._user_sensor_dims[i])
            glEndList()
            
        self.listLeds = []
        for i in range(3):
            self.listLeds += [glGenLists(1)]
            if not self.listLeds[i]:
                raise SystemError("""Unable to generate display list using glGenLists""")
            glNewList(self.listLeds[i], GL_COMPILE)
            glutSolidSphere(*self.cloud.settings.graphics._led_dims[i])
            glEndList()
    
    @property
    def xRotation(self):
        return self.xRot

    @property
    def yRotation(self):
        return self.yRot

    @property
    def zRotation(self):
        return self.zRot
    
    @xRotation.setter
    def xRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.xRot:
            self.xRot = angle
            self.updateGL()

    @yRotation.setter
    def yRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.yRot:
            self.yRot = angle
            self.updateGL()

    @zRotation.setter
    def zRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.zRot:
            self.zRot = angle
            self.updateGL()

    def mousePressEvent(self, event):
        self.mypaint(False)
        pixel = glReadPixels(event.pos().x(), self.height()-event.pos().y(), 1, 1, GL_RGB, GL_BYTE)
        r = str((_get_color_id(pixel[0][0].tolist())))
        try:
            d = self.color_dict[r]
            if d == self.selected_device:
                self.selected_device = None
            else:
                self.selected_device = d
        except KeyError:
            self.selected_device = None
            
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.xRotation = self.xRot + 8 * dy
            self.yRotation = self.yRot + 8 * dx
        elif event.buttons() & QtCore.Qt.RightButton:
            self.xRotation = self.xRot + 8 * dy
            self.zRotation = self.zRot + 8 * dx

        self.lastPos = event.pos()
    
    def save_image(self, image=True):
        if image:
            basedir = self.cloud.settings.runtime.dir_image
        else:
            basedir = self.cloud.settings.runtime.tmp_dir_video
        
        width, height = self.width(), self.height()
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixelsub(0, 0, width, height, GL_RGB)
        assert data.shape == (width,height,3), """Got back array of shape %r, expected %r"""%(
            data.shape,
            (width,height,3),
        )
        image = Image.fromstring( "RGB", (width, height), data.tostring())
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        dir = os.path.join(basedir, "%s" % self.start_time)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        filename = os.path.join(dir, "%s.png" % self.frameno)
        image.save(filename, "PNG")
    
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == QtCore.Qt.Key_I:
            self.save_image()
        if key == QtCore.Qt.Key_R:
            self.recording = True
        if key == QtCore.Qt.Key_S:
            self.recording = False
        sense_keys = [QtCore.Qt.Key_T, QtCore.Qt.Key_Y, QtCore.Qt.Key_U]
        for i in range(len(sense_keys)):
            if key == sense_keys[i]:
                if self.selected_device:
                    self.selected_device.senses[i] = not self.selected_device.senses[i]
                    self.updateGL()
                    
        if key == QtCore.Qt.Key_L:
            self.cloud.show_leds = not self.cloud.show_leds
            self.updateGL()
            
        dirs = {QtCore.Qt.Key_Left: [-1,0],
                QtCore.Qt.Key_Right: [1,0],
                QtCore.Qt.Key_Up: [0,1],
                QtCore.Qt.Key_Down: [0,-1]}
        for (k,v) in dirs.items():
            if key == k:
                glTranslatef(10*v[0], 10*v[1], 0)
                self.updateGL()
                
        if key == QtCore.Qt.Key_3:
            self.cloud.led_stacking_mode = (self.cloud.led_stacking_mode+1)%3
            self.updateGL()
            
        if key == QtCore.Qt.Key_B:
            self.cloud.show_body = not self.cloud.show_body
            self.updateGL()
            
    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(self.cloud.window_width, self.cloud.window_height)
    
    def paintGL(self):
        self.mypaint(True)
        
    def mypaint(self, real):
        self.set3dProjection(real)
        for d in self.cloud.devices:
            x = d.x
            y = d.y
            z = d.z
            glPushMatrix()
            glTranslatef(x,y,z)
            if real:
                if self.cloud.show_body:
                    glColor4f(*self.cloud.settings.graphics.simple_body_color)
                    glCallList(self.listSimpleBody)
                    for i in range(3):
                        if d.senses[i] != 0:
                            glColor4f(*self.cloud.settings.graphics._user_sensor_colors[i])
                            glCallList(self.listSenses[i])
                    if d == self.selected_device:
                        glColor4f(*self.cloud.settings.graphics.selected_device_color)
                        glCallList(self.listSelectedDevice)
                        
                if self.cloud.show_radio:
                    glColor4f(*self.cloud.settings.graphics.radio_range_ring_color)
                    glCallList(self.listRadio)
                
                if self.cloud.show_leds:
                    if self.cloud.led_blend:
                        if(d.leds != [0,0,0]):
                            glPushMatrix()
                            glTranslatef(0,0,0)
                            glColor3f(*d.leds)
                            glCallList(self.listBlendLed)
                            glPopMatrix()
                    else:
                        leds = [0,0,0]
                        if not self.cloud.led_flat:
                            if self.cloud.led_stacking_mode == pymorphous.implementation.simulator.constants.LED_STACKING_MODE_DIRECT:
                                acc = 0
                                for i in range(3):
                                    leds[i] = d.leds[i]+acc
                                    acc += d.leds[i]
                            elif self.cloud.led_stacking_mode == pymorphous.implementation.simulator.constants.LED_STACKING_MODE_OFFSET:
                                for i in range(3):
                                    leds[i] = d.leds[i]+i
                            else:
                                for i in range(3):
                                    leds[i] = d.leds[i]
                            
                        for i in range(3):
                            if d.leds[i] != 0:
                                glPushMatrix()
                                glTranslatef(0,0,leds[i])
                                glColor4f(*self.cloud.settings.graphics._led_colors[i])
                                glCallList(self.listLeds[i])
                                glPopMatrix()

            else:
                if self.cloud.show_body:
                    glColor3b(d.color_id.red, d.color_id.green, d.color_id.blue)
                    glCallList(self.listSelect)
            glPopMatrix()
        if real:
            if self.recording:
                self.save_image(image=False)
            self.frameno += 1
    
    def set3dProjection(self, real=True):
        glLoadIdentity();
        glViewport(0, 0, self.width(), self.height())
        if real:
            glClearColor(*self.cloud.settings.graphics.background_color)
        else:
            glClearColor(1,1,1,1)
            glDisable(GL_LIGHTING)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)
            glShadeModel(GL_FLAT)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45.0,float(self.width())/self.height(),0.1,200.0)    #setup lens
        glTranslatef(0, 0, -150.0)                #move back
        #glRotatef(60, 1, 60, 90)                       #orbit higher
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        
    def resizeGL(self, width, height):
        self.set3dProjection()
    
    def myupdate(self):
        now = time.time()
        delta = now - self.last_time
        self.cloud.update(delta)
        self.last_time = now
        self.updateGL()
    
    def normalizeAngle(self, angle):
        while (angle < 0):
            angle += 360 * 16

        while (angle > 360 * 16):
            angle -= 360 * 16
            
def simulator_graphics(cloud):
    app = QtGui.QApplication(sys.argv)
    window = _SimulatorWindow(cloud = cloud)
    window.show()
    sys.exit(app.exec_())
