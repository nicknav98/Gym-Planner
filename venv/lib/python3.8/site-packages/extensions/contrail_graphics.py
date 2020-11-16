import time

import numpy

import pymorphous.simulator_graphics

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


class Window(QtGui.QWidget):
    def __init__(self, cloud, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.glWidget = ContrailGLWidget(cloud)
        
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        self.setLayout(mainLayout)
        
        self.setWindowTitle(self.tr(cloud.window_title))
        
class ContrailGLWidget(pymorphous.simulator_graphics._SimulatorGLWidget):
    
    def __init__(self, cloud, parent=None):
        pymorphous.simulator_graphics._SimulatorGLWidget.__init__(self, cloud, parent)
        
        self.trail = {}
        for d in cloud.devices:
            self.trail[d] = []
    
    def __del__(self):
        self.makeCurrent()
        glDeleteLists(self.listSimpleBody, 1)
        
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)   
        glutInit()
        
        self.listTrailBody = glGenLists(1);
        if not self.listTrailBody:
            raise SystemError("""Unable to generate display list using glGenLists""")
        glNewList(self.listTrailBody, GL_COMPILE)
        glutSolidSphere(0.4, 8, 8)
        glEndList()

    def mousePressEvent(self, event):
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
    
    def set3dRotation(self):
        glLoadIdentity()
        glClearColor(0,0,0,1) 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
        glViewport(0,0,self.width(),self.height())

        glMatrixMode(GL_PROJECTION)
        
        gluPerspective(45.0,float(self.width())/self.height(),0.1,200.0)    #setup lens
        glTranslatef(0, 0, -150.0)                #move back
        #glRotatef(60, 1, 60, 90)                       #orbit higher
        
    def paintGL(self):
        self.set3dRotation()
        
        glPushMatrix()
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        for d in self.cloud.devices:
            for p in self.trail[d]:
                glPushMatrix()
                glTranslatef(p[0],p[1],p[2])
                glColor4f(1,1,1,1)
                glCallList(self.listTrailBody)
                glPopMatrix()
            self.trail[d] += [numpy.array(d.coord)]
        glPopMatrix()
        if self.recording:
            self.save_image(image=False)
        self.frameno += 1
    
    def resizeGL(self, width, height):
        self.set3dRotation()
            
def contrail_graphics(cloud):
    app = QtGui.QApplication(sys.argv)
    window = Window(cloud = cloud)
    window.show()
    sys.exit(app.exec_())
