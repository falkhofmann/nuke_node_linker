from PySide2 import QtWidgets


from nuke_node_linker import nuke_node_linker_ui_search as search
from nuke_node_linker import nuke_node_linker_model as model
from nuke_node_linker import constants

reload(search)
reload(model)


class Controller:

    def __init__(self, view):
        self.view = view

        self.links = model.get_all_linked_nodes('Link')
        self.bookmarks = model.get_all_linked_nodes('Bookmark')

        suffix_included = model.add_suffix(self.links.keys(), self.bookmarks.keys())

        self.view.user_input.fill_completer(suffix_included)

        self.set_up_signals()

    def set_up_signals(self):
        self.view.user_input.confirmed.connect(lambda text: self.confirm_selection(text))

    def confirm_selection(self, link):

        check_book = link.rpartition(' {}'.format(constants.BOOKMARK_SUFFIX))[0]
        check_link = link.rpartition(' {}'.format(constants.LINK_SUFFIX))[0]

        if check_book:
            model.jump_to_bookmark(self.bookmarks[check_book])

        elif check_link:
            model.create_link_node(self.links[check_link], link)


def start():
    """Start up function."""
    global VIEW  # pylint: disable=global-statement
    VIEW = search.NodeLinkerFind()
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)


def start_from_main():
    app = QtWidgets.QApplication()
    global VIEW  # pylint: disable=global-statement
    VIEW = search.NodeLinkerFind()
    VIEW.raise_()
    VIEW.show()
    Controller(VIEW)
    app.exec_()


if __name__ == '__main__':
    start_from_main()
