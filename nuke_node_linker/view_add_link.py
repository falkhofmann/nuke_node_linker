"""View for add link option."""

# Import third-party modules
from PySide2 import QtCore  # pylint: disable=import-error
from PySide2 import QtGui  # pylint: disable=import-error
from PySide2 import QtWidgets  # pylint: disable=import-error

# Import local modules
from nuke_node_linker import constants
from nuke_node_linker import utils


class Button(QtWidgets.QPushButton):
    def __init__(self, name):
        super(Button, self).__init__()
        self.setText(name)
        self.setMaximumSize(200, 30)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                           QtWidgets.QSizePolicy.Expanding)
        utils.set_style_sheet(self)


class AddLink(QtWidgets.QWidget):

    create = QtCore.Signal(object)

    def __init__(self, node):
        """Initialize Custom Widget."""
        super(AddLink, self).__init__()
        self.node = node

        self.set_window_properties()

        self.build_widgets()
        self.build_layouts()
        self.set_up_signal()

        self.link_name.setFocus()

    def set_window_properties(self):
        self.setFixedSize(400, 150)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Add NodeLink')

    def build_widgets(self):
        """Build widgets for interface."""
        self.color_bar = QtWidgets.QLabel()
        self.color_bar.setMaximumHeight(20)
        self.color_bar.setStyleSheet("font: 17px")

        self.dropdown_type = QtWidgets.QComboBox()
        model = self.dropdown_type.model()

        for index, item in enumerate(sorted(constants.KNOB_NAMES.keys())):
            if item == 'Linked':
                continue
            model.appendRow(QtGui.QStandardItem(item))
            icon_file = utils.get_icon_path(item)
            self.dropdown_type.setItemIcon(index, QtGui.QIcon(icon_file))

        self.dropdown_category = QtWidgets.QComboBox()
        model = self.dropdown_category.model()

        for index, item in enumerate(sorted(constants.COLORS.keys())):
            model.appendRow(QtGui.QStandardItem(item))

        self.link_name = QtWidgets.QLineEdit()
        self.link_name.setValidator(QtGui.QRegExpValidator(
            QtCore.QRegExp(constants.NAME_REGEX)))

        self.link_name.setPlaceholderText('name')
        self.cancel_button = Button('cancel')
        self.ok_button = Button('ok')

    def build_layouts(self):
        """Create and apply layouts."""
        top_bar_layout = QtWidgets.QHBoxLayout()
        top_bar_layout.addWidget(self.color_bar)

        category_layout = QtWidgets.QHBoxLayout()
        confirm_layout = QtWidgets.QHBoxLayout()

        category_layout.addWidget(self.dropdown_type)
        category_layout.addWidget(self.dropdown_category)
        category_layout.addWidget(self.link_name)

        confirm_layout.addWidget(self.cancel_button)
        confirm_layout.addWidget(self.ok_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_bar_layout)
        main_layout.addLayout(category_layout)
        main_layout.addLayout(confirm_layout)
        self.setLayout(main_layout)

    def set_up_signal(self):
        """Connect signals to methods."""
        self.link_name.returnPressed.connect(self.create_link)
        self.cancel_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.create_link)

    def create_link(self):
        self.create.emit((self.dropdown_type.currentText(),
                          self.dropdown_category.currentText(),
                          self.link_name.text(),
                          self.node))
        self.close()

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Route key press events and trigger actions accordingly.

        Args:
            event (QtGui.QWidget.keyPressEvent): Key pressed event.

        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
