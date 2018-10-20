# Import third-party modules
from PySide2 import QtWidgets

# Import local modules
from nuke_node_linker import view_add_link
from nuke_node_linker import model as model

from nuke_node_linker import constants

reload(view_add_link)
reload(model)


class Controller:

    def __init__(self, view):
        self.view = view
        self.view.dropdown_type.setCurrentIndex(1)
        self.set_up_signals()

    def set_up_signals(self):
        self.view.create.connect(lambda link_details: self.create_link(link_details))

    def create_link(self, link_details):
        print link_details
        type_, category, link_name, node = link_details
        sanity = model.sanity_check(node, constants.KNOB_NAMES[type_])
        if not sanity:
            return
        model.add_link_knob(node, constants.KNOB_NAMES[type_], category, link_name)


def start():
    """Start up function."""
    node = model.get_node()
    if not node:
        return

    global VIEW  # pylint: disable=global-statement
    VIEW = view_add_link.AddLink(node)
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)


def start_from_main():
    app = QtWidgets.QApplication()
    global VIEW  # pylint: disable=global-statement
    VIEW = view_add_link.AddLink([])
    VIEW.raise_()
    VIEW.show()
    Controller(VIEW)
    app.exec_()


if __name__ == '__main__':
    start_from_main()
