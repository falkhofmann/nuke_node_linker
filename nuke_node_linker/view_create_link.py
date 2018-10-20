import os
import sys


from PySide2 import QtCore  # pylint: disable=import-error
from PySide2 import QtGui  # pylint: disable=import-error
from PySide2 import QtWidgets  # pylint: disable=import-error


from nuke_node_linker.constants import WIDGET_COLORS


def nonconsec_find(needle, haystack, anchored=False):
    """checks if each character of "needle" can be found in order (but not
    necessarily consecutivly) in haystack.
    For example, "mm" can be found in "matchmove", but not "move2d"
    "m2" can be found in "move2d", but not "matchmove"
    """
    if len(haystack) == 0 and len(needle) > 0:
        # "a" is not in ""
        return False

    elif len(needle) == 0 and len(haystack) > 0:
        # "" is in "blah"
        return True

    # Turn haystack into list of characters (as strings are immutable)
    haystack = [hay for hay in str(haystack)]

    if anchored:
        if needle[0] != haystack[0]:
            return False
        else:
            # First letter matches, remove it for further matches
            needle = needle[1:]
            del haystack[0]

    for needle_atom in needle:
        try:
            needle_pos = haystack.index(needle_atom)
        except ValueError:
            return False
        else:
            # Dont find string in same pos or backwards again
            del haystack[:needle_pos + 1]
    return True


class UserLineInput(QtWidgets.QLineEdit):
    pressed_arrow = QtCore.Signal(str)
    cancelled = QtCore.Signal()

    def event(self, event):
        """Make tab trigger returnPressed

        Also emit signals for the up/down arrows, and escape.
        """

        is_keypress = event.type() == QtCore.QEvent.KeyPress

        if is_keypress and event.key() == QtCore.Qt.Key_Tab:
            # Can't access tab key in keyPressedEvent
            self.returnPressed.emit()
            return True

        elif is_keypress and event.key() == QtCore.Qt.Key_Up:
            # These could be done in keyPressedEvent, but.. this is already here
            self.pressed_arrow.emit("up")
            return True

        elif is_keypress and event.key() == QtCore.Qt.Key_Down:
            self.pressed_arrow.emit("down")
            return True

        elif is_keypress and event.key() == QtCore.Qt.Key_Escape:
            self.cancelled.emit()
            return True

        else:
            return super(UserLineInput, self).event(event)


class LinkModel(QtCore.QAbstractListModel):

    def __init__(self, all_links=[], all_bookmarks=[], filter_text = "", num_items=15):
        super(LinkModel, self).__init__()

        self._filter_text = filter_text
        self._all_links = all_links
        self._all_bookmarks = all_bookmarks
        self.num_items = num_items
        self._items = []
        self.update()

    def set_filter(self, filter_text):
        self._filter_text = filter_text
        self.update()

    def update(self):
        filtertext = self._filter_text.lower()


        scored = []
        all = self._all_bookmarks + self._all_links
        for link in all:

            if nonconsec_find(filtertext, link.lower(), anchored=True):
                if link in self._all_bookmarks:
                    type_ = 'Bookmark'
                else:
                    type_ = 'Link'
                scored.append({'text': link,
                               'type': type_})

        self._items = sorted(scored)
        self.modelReset.emit()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return min(self.num_items, len(self._items))

    def data(self, index, role=QtCore.Qt.DisplayRole):

        category = self._items[index.row()]['type']

        if role == QtCore.Qt.DisplayRole:
            return self._items[index.row()]['text']

        elif role == QtCore.Qt.BackgroundRole:
            return QtGui.QColor.fromHsvF(*WIDGET_COLORS[category])

        elif role == QtCore.Qt.DecorationRole:
            icon_file = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                        "icons",
                                                        "{}.png".format(category)))
            return QtGui.QPixmap(icon_file).scaled(QtCore.QSize(20, 20), QtCore.Qt.KeepAspectRatio)
        else:
            # Ignore other roles
            return None


class CreateLink(QtWidgets.QWidget):

    create = QtCore.Signal(object)

    def __init__(self):
        """Initialize Custom Widget."""
        super(CreateLink, self).__init__()

        self.set_window_properties()

        self.build_widgets()
        self.build_layouts()
        self.set_up_signal()

    def set_window_properties(self):
        self.setFixedSize(400, 150)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Add NodeLink')

    def build_widgets(self):
        """Build widgets for interface."""
        self.input = UserLineInput()
        self.list_view = QtWidgets.QListView()

    def build_layouts(self):
        """Create and apply layouts."""
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.input)
        main_layout.addWidget(self.list_view)

        self.setLayout(main_layout)

    def set_up_signal(self):
        self.input.textChanged.connect(self.update)

    def set_up_model(self, all_links, all_bookmarks):
        self.model = LinkModel(all_links=all_links, all_bookmarks=all_bookmarks)
        self.list_view.setModel(self.model)

    def update(self, text):
        """On text change, selects first item and updates filter text
        """
        # self.list_view.setCurrentIndex(self.model.index(0))
        self.model.set_filter(text)

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Route key press events and trigger actions accordingly.

        Args:
            event (QtGui.QWidget.keyPressEvent): Key pressed event.

        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


def start_from_main():
    app = QtWidgets.QApplication(sys.argv)
    global interface  # pylint: disable=global-statement
    interface = CreateLink()
    interface.set_up_model(all_links=['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrott'],
                           all_bookmarks=['Alfab', 'Bravob', 'Charlieb', 'Deltab', 'Echob', 'Foxtrottb'])
    interface.show()
    app.exec_()


if __name__ == '__main__':
    start_from_main()
