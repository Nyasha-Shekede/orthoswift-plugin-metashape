import sys
import types


def pytest_configure(config):
    """Ensure Metashape and PySide2 mock stubs are available for headless test execution."""
    if "Metashape" not in sys.modules:
        metashape = types.ModuleType("Metashape")
        app = types.ModuleType("Metashape.app")
        app.version = "2.2.0"
        app.addMenuItem = lambda *a, **k: None
        app.document = None
        metashape.app = app
        metashape.ImageCompression = lambda: types.SimpleNamespace(tiff_tiled=True, tiff_overviews=True)
        metashape.RasterFormatTiles = 1
        metashape.ImageFormatTIFF = 1
        metashape.OrthomosaicData = 1
        sys.modules["Metashape"] = metashape

    if "PySide2" not in sys.modules:
        pyside2 = types.ModuleType("PySide2")
        qtcore = types.ModuleType("PySide2.QtCore")
        qtgui = types.ModuleType("PySide2.QtGui")
        qtwidgets = types.ModuleType("PySide2.QtWidgets")

        class QObject:
            def __init__(self, parent=None):
                self.parent = parent

        class QWidget(QObject):
            def __init__(self, parent=None):
                super().__init__(parent)
            def setStyleSheet(self, s): pass
            def setObjectName(self, n): pass
            def setVisible(self, v): pass
            def setMaximumWidth(self, w): pass
            def setLayout(self, l): pass

        class QDialog(QWidget):
            Accepted = 1
            Rejected = 0
            def __init__(self, parent=None):
                super().__init__(parent)
            def setWindowTitle(self, t): pass
            def setWindowFlags(self, f): pass
            def windowFlags(self): return 0
            def resize(self, w, h): pass
            def setMinimumWidth(self, w): pass
            def exec_(self): return 1
            def accept(self): pass
            def reject(self): pass

        class QLabel(QWidget):
            def __init__(self, text="", parent=None):
                super().__init__(parent)
                self.text = text
            def setText(self, t): self.text = t
            def setWordWrap(self, w): pass
            def setAlignment(self, a): pass
            def setFixedWidth(self, w): pass
            def setSizePolicy(self, h, v): pass
            def setFont(self, f): pass

        class QPushButton(QWidget):
            def __init__(self, text="", parent=None):
                super().__init__(parent)
                self.text = text
                self.clicked = types.SimpleNamespace(connect=lambda f: None)
            def setText(self, t): self.text = t
            def setEnabled(self, e): pass

        class QLineEdit(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self._text = ""
            def text(self): return self._text
            def setText(self, t): self._text = t
            def setPlaceholderText(self, t): pass
            def setValidator(self, v): pass

        class QComboBox(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self._items = []
                self.currentIndexChanged = types.SimpleNamespace(connect=lambda f: None)
            def addItems(self, items): self._items.extend(items)
            def currentText(self): return self._items[0] if self._items else ""

        class QCheckBox(QWidget):
            def __init__(self, text="", parent=None):
                super().__init__(parent)
                self._checked = False
                self.stateChanged = types.SimpleNamespace(connect=lambda f: None)
            def isChecked(self): return self._checked
            def setChecked(self, c): self._checked = bool(c)

        class QLayout:
            def __init__(self, parent=None): pass
            def addWidget(self, w, *a): pass
            def addLayout(self, l, *a): pass
            def addStretch(self, *a): pass
            def setContentsMargins(self, *a): pass
            def setSpacing(self, *a): pass
            def setAlignment(self, *a): pass

        class QVBoxLayout(QLayout): pass
        class QHBoxLayout(QLayout): pass

        class QFrame(QWidget):
            HLine = 1
            def setFrameShape(self, s): pass

        class QScrollArea(QWidget):
            def setWidgetResizable(self, r): pass
            def setWidget(self, w): pass

        class QTableWidget(QWidget):
            def __init__(self, rows=0, cols=0, parent=None):
                super().__init__(parent)
            def setHorizontalHeaderLabels(self, l): pass
            def verticalHeader(self):
                return types.SimpleNamespace(setVisible=lambda v: None, setSectionResizeMode=lambda *a: None)
            def horizontalHeader(self):
                return types.SimpleNamespace(setSectionResizeMode=lambda *a: None)
            def setEditTriggers(self, t): pass
            def setSelectionMode(self, m): pass
            def setShowGrid(self, g): pass
            def setWordWrap(self, w): pass
            def setTextElideMode(self, m): pass
            def setSizePolicy(self, *a): pass
            def setMinimumHeight(self, h): pass
            def setItem(self, r, c, i): pass

        class QTableWidgetItem:
            def __init__(self, text=""):
                self.text = text
            def setForeground(self, c): pass
            def font(self):
                return types.SimpleNamespace(setBold=lambda b: None)
            def setFont(self, f): pass

        class QProgressDialog(QWidget):
            def __init__(self, label="", cancel="", min=0, max=100, parent=None):
                super().__init__(parent)
                self.canceled = types.SimpleNamespace(connect=lambda f: None)
            def setWindowTitle(self, t): pass
            def setWindowFlags(self, f): pass
            def resize(self, w, h): pass
            def setWindowModality(self, m): pass
            def setMinimumDuration(self, d): pass
            def setValue(self, v): pass
            def setLabelText(self, t): pass
            def isVisible(self): return True
            def show(self): pass
            def close(self): pass
            def deleteLater(self): pass

        class QProcessEnvironment:
            @staticmethod
            def systemEnvironment():
                return types.SimpleNamespace(value=lambda k, d="": d, insert=lambda k, v: None)

        class QProcess(QObject):
            NormalExit = 0
            def __init__(self, parent=None):
                super().__init__(parent)
                self.readyReadStandardOutput = types.SimpleNamespace(connect=lambda f: None)
                self.readyReadStandardError = types.SimpleNamespace(connect=lambda f: None)
                self.finished = types.SimpleNamespace(connect=lambda f: None)
            def setProcessEnvironment(self, e): pass
            def start(self, prog, args): pass
            def waitForStarted(self, timeout=5000): return True
            def kill(self): pass
            def deleteLater(self): pass

        class QTimer(QObject):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.timeout = types.SimpleNamespace(connect=lambda f: None)
            def setInterval(self, ms): pass
            def start(self): pass
            def stop(self): pass

        class QApplication:
            _instance = None
            @classmethod
            def instance(cls):
                if not cls._instance: cls._instance = QApplication()
                return cls._instance
            @classmethod
            def activeWindow(cls): return None
            @classmethod
            def processEvents(cls): pass

        qtcore.Qt = types.SimpleNamespace(
            WindowMaximizeButtonHint=1, WindowMinimizeButtonHint=2,
            WindowContextHelpButtonHint=4, CustomizeWindowHint=8,
            WindowModal=1, AlignTop=1, AlignLeft=2, Checked=2, Unchecked=0,
            ElideNone=0
        )
        qtcore.QProcess = QProcess
        qtcore.QProcessEnvironment = QProcessEnvironment
        qtcore.QTimer = QTimer
        qtcore.QUrl = types.SimpleNamespace(fromLocalFile=lambda f: f)

        qtgui.QFont = lambda: types.SimpleNamespace(
            setFamilies=lambda f: None, setPixelSize=lambda s: None,
            setWeight=lambda w: None, setItalic=lambda i: None,
            setLetterSpacing=lambda *a: None
        )
        qtgui.QFont.ExtraBold = 800
        qtgui.QFont.PercentageSpacing = 1
        qtgui.QColor = lambda c: c
        qtgui.QFontDatabase = types.SimpleNamespace(addApplicationFont=lambda f: 1)
        qtgui.QDesktopServices = types.SimpleNamespace(openUrl=lambda u: True)
        qtgui.QDoubleValidator = lambda *a: None

        qtwidgets.QApplication = QApplication
        qtwidgets.QWidget = QWidget
        qtwidgets.QDialog = QDialog
        qtwidgets.QLabel = QLabel
        qtwidgets.QPushButton = QPushButton
        qtwidgets.QLineEdit = QLineEdit
        qtwidgets.QComboBox = QComboBox
        qtwidgets.QCheckBox = QCheckBox
        qtwidgets.QFrame = QFrame
        qtwidgets.QScrollArea = QScrollArea
        qtwidgets.QTableWidget = QTableWidget
        qtwidgets.QTableWidgetItem = QTableWidgetItem
        qtwidgets.QProgressDialog = QProgressDialog
        qtwidgets.QVBoxLayout = QVBoxLayout
        qtwidgets.QHBoxLayout = QHBoxLayout
        qtwidgets.QSizePolicy = types.SimpleNamespace(Expanding=1, Minimum=2, Preferred=3)
        qtwidgets.QAbstractItemView = types.SimpleNamespace(NoEditTriggers=0, NoSelection=0)
        qtwidgets.QHeaderView = types.SimpleNamespace(ResizeToContents=0, Stretch=1)
        qtwidgets.QFileDialog = types.SimpleNamespace(getOpenFileName=lambda *a, **k: ("", ""))

        pyside2.QtCore = qtcore
        pyside2.QtGui = qtgui
        pyside2.QtWidgets = qtwidgets

        sys.modules["PySide2"] = pyside2
        sys.modules["PySide2.QtCore"] = qtcore
        sys.modules["PySide2.QtGui"] = qtgui
        sys.modules["PySide2.QtWidgets"] = qtwidgets


pytest_configure(None)
