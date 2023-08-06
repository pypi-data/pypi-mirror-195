import qrcode, logging, tempfile, os, sys, shlex
from time import sleep
from os.path import join
from io import StringIO
import zeroconf
from zeroconf import ServiceBrowser, Zeroconf
from importlib.resources import files as resource
from sh import adb, ErrorReturnCode
from PyQt6.QtWidgets import ( QApplication,
                              QLabel,
                              QPushButton,
                              QVBoxLayout,
                              QHBoxLayout,
                              QDialog,
                              QWidget,
                              QSizePolicy )
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt, QDir, QPoint, pyqtSlot, pyqtSignal, QObject, QThread, QSize
from . import images

log = logging.getLogger(__name__)

OUT = StringIO()
ERR = StringIO()
ZC_output = StringIO()

class ListenerSignals(QObject):
    ADBconnect = pyqtSignal(object)

class Listener:
    def __init__(self):
        log.debug("Initiating Listener for zeroconf")
        self.sig = ListenerSignals()

    def update_service(self, zeroconf, type, name):
        log.info( f"Service {name} updated" )

    def remove_service(self, zeroconf, type, name):
        log.info( f"Service {name} removed." )

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        log.info( f"Service {name} added" )
        log.info( f"Service Info: {info}" )
        self.sig.ADBconnect.emit(info)

class ServiceSignals(QObject):
    _exit = pyqtSignal()
    finished = pyqtSignal()
    scanned = pyqtSignal()
    timeout = pyqtSignal()

class Service(QThread):
    """
    Main class ran in separate thread
    """
    FINISHED = False
    TIMEOUT = 15
    CONNECTING = False

    def __init__(self, key, *, timeout = 15):
        """
        timeout = [n] seconds
        """
        super().__init__()
        log.debug("Initiating Service")
        zeroconf.log.setLevel(20)
        self.TIMEOUT = timeout
        self.key = key

        self.listener = Listener()
        self.listener.sig.ADBconnect.connect( self.adb_connect )

        self.sig = ServiceSignals()
        self.sig._exit.connect( self._finished )

    def run(self):
        """
        FORMAT_QR = "WIFI:T:ADB;S:%s;P:%s;;"
        """
        TYPE = "_adb-tls-pairing._tcp.local."

        log.debug("Initializing Zeroconf and ServiceBrowser")
        self.zeroconf = Zeroconf()
        browser = ServiceBrowser(self.zeroconf, TYPE, self.listener)

        log.debug("Started zeroconf")
        log.info("Scan QR code to pair new devices.")
        log.info("[Developer options]-[Wireless debugging]-[Pair device with QR code]")

        TO = self.TIMEOUT
        try:
            while True:
                if self.FINISHED:
                    break
                if TO < 0:
                    raise RuntimeError
                sleep(0.5)
                if self.CONNECTING:
                    continue
                TO -= 0.5
                if TO in (0,1,2,3,4,5):
                    log.warning(f"Timeout in {TO} seconds")
                elif TO <= 30 and TO % 10 == 0:
                    log.info(f"Timeout in {TO} seconds")
        except RuntimeError:
            log.error(f"Timed out after {self.TIMEOUT} seconds")
            self.sig.timeout.emit()
        except Exception as E:
            log.exception(E)
            raise E
        finally:
            self.zeroconf.close()

    @pyqtSlot(object)
    def adb_connect(self, info):
        self.CONNECTING = True
        self.sig.scanned.emit()
        adb( 'kill-server' )
        adb( 'start-server' )
        sleep(0.1)
        log.info( "Running 'adb pair...'" )
        adb( 'pair', f"{info.server}:{info.port}", shlex.quote(self.key), _out = OUT, _err = ERR )
        out = OUT.getvalue()
        err = ERR.getvalue()
        if out:
            log.info(out)
        if err:
            log.error(err)

        self.sig.finished.emit()

    def _finished(self):
        self.FINISHED = True

class AllDone(QDialog):
    style = """
            QLabel#title {
                font: 18pt bold;
                color: #868686;
            }
            QLabel#msg {
                font: 12pt;
                color: #476460;
            }
            QPushButton#quit {
                border: 4px outset #999999;
                border-radius: 5px;
                background-color: #86a786;
                font: 12pt bold #222222;
                ::pressed {
                    font: 12pt bold #ababab;
                    border: 4px inset #222222;
                    border-radius: 5px;
                    background-color: #202820;
                }
            }
            """
    ERR_style = """
                QLabel#title {
                    font: 18pt bold;
                    color: #ff0000;
                }
                QLabel#msg {
                    font: 12pt;
                    color: #aa0000;
                }
                QPushButton#quit {
                    font: 14pt bold;
                    color: #222222;
                    border: 4px outset #999999;
                    border-radius: 5px;
                    background-color: #bd4f45;
                }
                QPushButton#quit::pressed {
                    font: 14pt bold;
                    color: #ababab;
                    border: 4px inset #222222;
                    border-radius: 5px;
                    background-color: #281915;
                }
                """

    def __init__(self, parent = None, *, cancel = False, timeout = 0):
        log.debug("Initiating AllDone GUI")
        super().__init__(parent)

        win_icon = QIcon( resource( images ).joinpath( 'android.png' ).as_posix() )

        self.setWindowTitle(f"QrConnect")
        self.setWindowIcon(win_icon)

        layout = QVBoxLayout(self)
        layout.addSpacing(20)

        self.title = QLabel(self)
        self.title.setObjectName('title')
        self.title.setFixedHeight(30)
        self.title.setAlignment( Qt.AlignmentFlag.AlignCenter )

        layout.addWidget( self.title )
        layout.addSpacing(20)

        self.msg = QLabel(self)
        self.msg.setObjectName('msg')
        self.msg.setText('')
        self.msg.setAlignment( Qt.AlignmentFlag.AlignCenter )

        layout.addWidget( self.msg )
        layout.addSpacing(40)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()

        self.btn = QPushButton(self)
        self.btn.setObjectName('quit')
        self.btn.setText("Quit")
        self.btn.setFixedSize(160,40)
        self.btn.clicked.connect( self.accept )

        btnLayout.addWidget( self.btn )
        btnLayout.addSpacing(10)
        layout.addLayout( btnLayout )
        log.debug(f"Setting up AllDone GUI - cancel = '{cancel}'")
        if cancel:
            self.setStyleSheet( self.ERR_style )
            self.title.setText( "Pairing Cancelled" )
        elif timeout:
            self.setStyleSheet( self.ERR_style )
            self.title.setText( "Timeout Error" )
            self.msg.setText( f"Pairing timed out after {timeout} seconds" )
        else:
            info = self.getInfo()
            self.title.setText( info['title'] )
            self.msg.setText( info['message'] )

        self.show()

    def getInfo(self):
        _list = []

        def getDev():
            for i in _list:
                if re.match( '^[0-9]+\.[0-9]+\.[0-9]+.+', i ):
                    return i
            log.error("No devices found after scan")
            return { 'title'  : "Error",
                     'message': "Error while trying to connect to device" }

        try:
            log.debug("Gathering devices after scan")
            _list = adb('devices', '-l', _err = ERR).strip().split('\n')[1:]
        except ErrorReturnCode:
            log.error( ERR.getvalue() )
            ioReset('err')

        dev = getDev()
        if isinstance( dev, dict ):
            self.setStyleSheet( self.ERR_style )
            return dev
        self.setStyleSheet( self.style )

        serial, info = dev.split(' ', 1)
        data = dict([(i[0], i[1]) for i in [ q.split(':') for q in info.split()[1:] ]])
        device = { 'ip'   : serial.split(':')[0],
                   'port' : serial.split(':')[1],
                   **data    }

        log.debug("Returning found tcp device")
        return { 'title'  : "Connection Successful!",
                 'message': '<br>'.join([ f"Device:     {device['device']}",
                                          f"Model #:    {device['model']}",
                                          f"IP Address: {device['ip']}",
                                          f"Port:       {device['port']}" ])}

class ImageLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setAlignment( Qt.AlignmentFlag.AlignCenter )
        self.setSizePolicy( QSizePolicy.Policy.Expanding,
                            QSizePolicy.Policy.Expanding )

    def loadImage(self, image):
        log.debug("Loading QPixmap image")
        self.image = image
        self.setPixmap( self.image )
        self.repaint()

    def resizeEvent(self, e):
        size = self.size()
        scaledPix = self.image.scaled( size,
                                       Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation )
        self.setPixmap( scaledPix )
        self.repaint()

        return super().resizeEvent(e)

class Viewer(QDialog):
    """
    Display the qr code for ADB
    """
    scanned = pyqtSignal()
    COMPLETED = False
    CANCELLED = False

    def __init__(self, parent = None):
        log.debug("Initiating Viewer gui")
        super().__init__(parent = parent)
        self.scanned.connect( self._scanned )

    def setupUI(self, pixmap):
        style = """
                QLabel#title {
                    font: 18pt bold;
                    color: #868686;
                }
                QPushButton#cancel {
                    font: 14pt bold;
                    color: #222222;
                    border: 4px outset #999999;
                    border-radius: 5px;
                    background-color: #bd4f45;
                }
                QPushButton#cancel::pressed {
                    font: 14pt bold;
                    color: #ababab;
                    border: 4px inset #222222;
                    border-radius: 5px;
                    background-color: #281915;
                }
                """

        win_icon = QIcon( resource( images ).joinpath( 'android.png' ).as_posix() )

        self.setWindowTitle(f"QrConnect")
        self.setWindowIcon(win_icon)
        self.setMinimumSize(380,456)
        self.resize( self.minimumSize() )
        self.setWindowModality( Qt.WindowModality.ApplicationModal )
        self.setStyleSheet(style)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5,5,5,5)
        layout.setAlignment( Qt.AlignmentFlag.AlignCenter )

        title = QLabel(self)
        title.setObjectName('title')
        title.setFixedHeight(30)
        title.setAlignment( Qt.AlignmentFlag.AlignCenter )

        layout.addWidget( title )
        layout.addSpacing(10)

        self.imageBox = ImageLabel(self)
        layout.addWidget( self.imageBox )

        # layout.addStretch()
        layout.addSpacing(10)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch()

        self.btn = QPushButton(self)
        self.btn.setObjectName('cancel')
        self.btn.setText("Cancel")
        self.btn.setFixedSize(160,40)
        self.btn.clicked.connect( self._cancel )

        btnLayout.addWidget( self.btn )
        btnLayout.addSpacing(40)
        layout.addLayout( btnLayout )

        if not pixmap:
            log.error("Pixmap image is empty")
        else:
            self.imageBox.loadImage(pixmap)

        centerWindow(self)
        log.debug("Showing image viewer GUI")
        self.show()

    def _scanned(self):
        self.COMPLETED = True
        self.accept()

    def _cancel(self):
        log.warning("Scan has been cancelled by user")
        self.CANCELLED = True
        self.accept()

    def closeEvent(self, e):
        if not self.COMPLETED:
            log.warning("Scan has been cancelled by user")
            self.CANCELLED = True

        if self.isActiveWindow():
            self.accept()

class Main(QObject):
    exit_code = 0
    viewFinished = False
    CONNECTED = False
    FINISHING = False

    def __init__(self, name = 'QrConnect', *, timeout = 30):
        super().__init__()
        key = self.createKey()

        log.debug("Initiating Main")
        self.timeout = timeout
        self.service = Service( key, timeout = int( timeout ))

        log.debug("Connecting signals")
        self.viewer = Viewer()
        self.viewer.accepted.connect( self.viewerClosed )

        self.service.sig.scanned.connect( self.closeQR )
        self.service.sig.finished.connect( self.connected )
        self.service.sig.timeout.connect( self.timeoutError )

        try:
            log.debug("Starting serviceThread")
            self.service.start()
        except InterruptedError:
            self.exit_code = 127
            log.error("Main interrupted by user")
            raise InterruptedError
        except Exception as E:
            self.exit_code = 1
            log.exception(E)
            raise E

        img = self.createQR( name, key )

        self.viewer.setupUI( img )
        self.viewer.exec()

    def createKey(self):
        log.debug("Creating password key")
        tmp = tempfile.NamedTemporaryFile()
        adb( 'keygen', tmp.name )
        with open( tmp.name, 'r' ) as f:
            key = ''.join( f.read().strip().split('\n')[1:-1] )
        tmp.close()
        log.info("Password key created")
        return key

    def createQR(self, name, key):
        log.debug("Creating qr image")
        img = qrcode.make( f"WIFI:T:ADB;S:{name};P:{key};;" )
        imgtmp = tempfile.NamedTemporaryFile( suffix = '.png', delete = False )
        img.save( imgtmp.name )
        log.debug(f"QR image saved to '{imgtmp.name}'")

        log.debug("Setting qr image to QPixmap")
        pixmap = QPixmap( imgtmp.name )
        if pixmap:
            log.info("QR image created")
            return pixmap
        else:
            log.error("QR image could not be applied to QPixmap")
            return QPixmap()

    @pyqtSlot()
    def timeoutError(self):
        if self.viewFinished:
            return
        self.viewFinished = True
        if self.viewer.isActiveWindow():
            self.viewer.accept()

        self.service.sig._exit.emit()

        alldone = AllDone( timeout = self.timeout )
        alldone.exec()
        self.exit_code = 3

    @pyqtSlot()
    def closeQR(self):
        self.viewer.scanned.emit()
        return self.viewerClosed()

    @pyqtSlot()
    def viewerClosed(self):
        if self.viewFinished:
            return
        self.viewFuncRan = True
        if self.viewer.COMPLETED:
            return self.completed()
        else:
            return self.cancelled()

    def cancelled(self):
        self.viewFinished = True
        self.service.sig._exit.emit()
        alldone = AllDone( cancel = True )
        alldone.exec()
        self.exit_code = 1

    def completed(self):
        if self.FINISHING:
            return
        self.FINISHING = True
        c = 0
        while self.service.CONNECTING and c < 150:
            try:
                sleep(0.2)
                if self.CONNECTED:
                    break
                c += 1
            except InterruptedError:
                break
            except Exception as E:
                log.exception(E)
                raise E
        if not self.viewer.COMPLETED:
            return self.cancelled()
        self.service.sig._exit.emit()
        alldone = AllDone()
        alldone.exec()
        self.exit_code = 0

    @pyqtSlot()
    def connected(self):
        self.CONNECTED = True

def centerWindow(obj):
    log.debug(f"Centering window")
    qr = obj.frameGeometry()
    cp = obj.screen().availableGeometry().center()
    qr.moveCenter(cp)
    obj.move(qr.topLeft())

if __name__ == '__main__':
    opts = sys.argv[1:]
    timeout = 15
    name = "QrConnect"

    if '--help' in opts:
        o = [( '--debug', "- Enable debugging mode" ),
             ( '--help', "- This help message" ),
             ( '--name', "- Name of connection to create" ),
             ( '', "\x1b[0;3m    - defaults to 'QrConnect'" ),
             ( '--timeout', "- Seconds to keep qrcode visible" ),
             ( '', "\x1b[0;3m    - defaults to 15 seconds" )]

        print( '\n'.join([ '', "        \x1b[1;37;4mQrConnect\x1b[0m",
                           *[ f"\x1b[1;33m{i[0]:>20}\x1b[2;37;3m {i[1]}\x1b[0m" for i in o ],
                           '' ]))
        sys.exit(0)

    if '--debug' in opts:
        log.set_format('debug')

    if '--timeout' in opts:
        try:
            index = opts.index('--timeout')
            timeout = int(opts[index+1])
        except IndexError:
            log.error(f"Option '{opts[index]}' requires an argument")
        except TypeError:
            log.error(f"Invalid argument '{opts[index+1]}' - expected number os seconds")

    if '--name' in opts:
        try:
            index = opts.index('--name')
            name = opts[index+1]
        except IndexError:
            log.error(f"Option '{opts[index]}' requires an argument")

    app = QApplication(sys.argv)
    X = 0
    try:
        main = Main( name, timeout = timeout )
        main.service.wait()
        X = main.exit_code
    except InterruptedError:
        log.error("Pairing interrupted by user")
        X = 130
    except Exception as E:
        log.exception(E)
        X = 2
    finally:
        sys.exit( X )
