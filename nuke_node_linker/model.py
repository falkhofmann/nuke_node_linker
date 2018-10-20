import nuke

from nuke_node_linker import constants
from nuke_node_linker.constants import KNOB_NAMES, LINK_NODE_TYPE


def get_node():
    """Get all selected nodes."""
    try:
        return nuke.selectedNode()
    except IndexError:
        nuke.message('Please select a node to create a link.')


def get_all_linked_nodes(category):
    """Gather all nodes which have node_link knob.

    Returns:
        list: Nuke nodes containing node_link knob.

    """
    return {node[KNOB_NAMES[category]].value(): node for node in nuke.allNodes() if KNOB_NAMES[category] in node.knobs()}
    # return [node for node in nuke.allNodes() if KNOB_NAMES[category] in node.knobs()]


def sanity_check(node, category):
    if category in node.knobs():
        return False
    else:
        return True


def add_link_knob(node, category, link_name):
    """
    Args:
        node (nuke.Node): Node to add node_link to.
        category (str): Category Constant.
        link_name (str): Additional user description.

    """
    if not has_node_tab(node):
        add_node_link_tab(node)

    link_knob = nuke.Text_Knob(category,  category, link_name)
    node.addKnob(link_knob)


def has_node_tab(node):
    """Check if node link tab already exists.

    Args:
        node (nuke.Node): Node to check for knobs.

    Returns:
        bool: True if tab exists, otherwise false.

    """
    if constants.TAB_NAME in node.knobs():
        return True
    else:
        return False


def add_node_link_tab(node):
    node.addKnob(nuke.Tab_Knob(constants.TAB_NAME))


def create_link_node(node, link_name):
    """Create NoOp node and connect to the given node.

    Add PyScript buttons to NoOp node.

    Args:
        node (nuke.Node): Node  to connect to.

    """
    link = nuke.createNode(LINK_NODE_TYPE)
    add_node_link_tab(link)

    if not node['tile_color'].value():
        tile_color = constants.LINKED_NODE_DEFAULT_COLOR
    else:
        tile_color = node['tile_color'].value()

    link.knob('hide_input').setValue(True)
    link['tile_color'].setValue(tile_color)
    link['label'].setValue('NodeLink: {}'.format(link_name))

    add_jump_buttons(link)

    link.setInput(0, node)


def add_jump_buttons(link):
    jump_to_input_node = ('from nuke_node_linker import nuke_node_linker_model as model;'
                          'model.jump_to_source(nuke.thisNode())')

    node_open = 'nuke.show(nuke.thisNode().input(0))'

    label = '<font size="3" color="orange">  {}  </font>'

    jump_knob = nuke.PyScript_Knob('jump',
                                   label.format('jump to source'),
                                   jump_to_input_node)

    open_knob = nuke.PyScript_Knob('open_properties',
                                   label.format('open link properties'),
                                   node_open)

    link.addKnob(jump_knob)
    link.addKnob(open_knob)


def jump_to_bookmark(node):

    nuke.zoom(2, [node.xpos(), node.ypos()])


def jump_to_source(node):
    """Zoom inside nodegraph to given node.

    Args:
        node (nuke.Node): Node to zoom to.

    """
    nuke.zoom(2, [node.input(0).xpos(), node.input(0).ypos()])


def add_suffix(links, bookmarks):

    link = ['{} {}'.format(link, constants.LINK_SUFFIX) for link in links]

    books = ['{} {}'.format(bm, constants.BOOKMARK_SUFFIX) for bm in bookmarks]

    return link + books
