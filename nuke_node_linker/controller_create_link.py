# Import third-party modules
from PySide2 import QtWidgets

# Import local modules
from nuke_node_linker import view_create_link
from nuke_node_linker import model

reload(view_create_link)
reload(model)


class Controller:

    def __init__(self, view):
        self.view = view

        self.links = model.get_all_linked_nodes('Link')
        self.bookmarks = model.get_all_linked_nodes('Bookmark')
        self.view.set_up_model(self.links, self.bookmarks)

        self.set_up_signals()

    def set_up_signals(self):
        self.view.create.connect(lambda x: self.create_item(x))

    def create_item(self, item):

        if item['type'] == 'Bookmark':
            model.jump_to_node(self.bookmarks[item['text']][0])

        elif item['type'] == 'Link':
            model.create_link_node(self.links[item['text']], item['text'])

        self.view.close()


def start():
    """Start up function."""
    global VIEW  # pylint: disable=global-statement
    VIEW = view_create_link.CreateLink()
    VIEW.raise_()
    VIEW.under_cursor()
    VIEW.show()

    Controller(VIEW)


def start_from_main():
    app = QtWidgets.QApplication()
    global VIEW  # pylint: disable=global-statement
    VIEW = view_create_link.CreateLink()
    VIEW.raise_()
    VIEW.show()
    Controller(VIEW)
    app.exec_()


if __name__ == '__main__':
    start_from_main()
