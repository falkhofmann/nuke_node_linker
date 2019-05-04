"""Controller to connect between view and model."""

# Import local modules
from nuke_node_linker import constants
from nuke_node_linker import model
from nuke_node_linker import view_add_link


class Controller:

    def __init__(self, view):
        self.view = view
        self.view.dropdown_type.setCurrentIndex(1)
        self.set_up_signals()

    def set_up_signals(self):
        """Connect signals to actions."""
        self.view.create.connect(lambda link_details: self.create_link(link_details))

    def create_link(self, link_details):
        """Create links based on given details and node.

        Args:
            link_details (tuple): Main type, Category, link name, node to create links from.

        """
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

    global VIEW
    VIEW = view_add_link.AddLink(node)
    VIEW.raise_()
    VIEW.show()

    Controller(VIEW)
