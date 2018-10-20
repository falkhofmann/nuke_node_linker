from PySide2 import QtWidgets


from nuke_node_linker import nuke_node_linker_ui_add as add
from nuke_node_linker import nuke_node_linker_model as model

from nuke_node_linker import constants

reload(add)
reload(model)


class Controller:

    def __init__(self, view):
        self.view = view
        self.view.dropdown.setCurrentIndex(1)
        self.set_up_signals()

    def set_up_signals(self):

        self.view.create.connect(lambda link_details: self.create_link(link_details))

    def create_link(self, link_details):
        type_, link_name, node = link_details
        sanity = model.sanity_check(node, constants.KNOB_NAMES[type_])
        if not sanity:
            return
        model.add_link_knob(node, constants.KNOB_NAMES[type_], link_name)


def start():
    """Start up function."""
    node = model.get_node()
    if not node:
        return

    global VIEW  # pylint: disable=global-statement
    VIEW = add.AddLink(node)
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)


def start_from_main():
    app = QtWidgets.QApplication()
    global VIEW  # pylint: disable=global-statement
    VIEW = add.AddLink([])
    VIEW.raise_()
    VIEW.show()
    Controller(VIEW)
    app.exec_()


if __name__ == '__main__':
    start_from_main()
