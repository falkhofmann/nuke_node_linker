# Import third-party modules
import nuke
import nukescripts

# Import local modules

from nuke_node_linker.constants import COLORS, KNOB_NAMES, LINK_NODE_TYPE, TAB_NAME


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
    return {node[KNOB_NAMES[category]].value(): (node, node[KNOB_NAMES[category]].label()) for node in nuke.allNodes() if KNOB_NAMES[category] in node.knobs()}


def sanity_check(node, category):
    if category in node.knobs():
        return False
    else:
        return True


def add_link_knob(node, type_, category, link_name):
    """
    Args:
        node (nuke.Node): Node to add node_link to.
        category (str): Category Constant.
        link_name (str): Additional user description.

    """
    if not link_name:
        return
    if not has_node_tab(node):
        add_node_link_tab(node)

    node.addKnob(nuke.Text_Knob(type_, category, link_name))


def has_node_tab(node):
    """Check if node link tab already exists.

    Args:
        node (nuke.Node): Node to check for knobs.

    Returns:
        bool: True if tab exists, otherwise false.

    """
    if TAB_NAME in node.knobs():
        return True
    else:
        return False


def add_node_link_tab(node):
    """Add custom tab knob to node.

    Args:
        node (nuke.Node): Node to add link knob to.

    """
    node.addKnob(nuke.Tab_Knob(TAB_NAME))


def create_link_node(node_details, link_name):
    """Create NoOp node and connect to the given node.

    Add PyScript buttons to NoOp node.

    Args:
        node_details (tuple): Node to connect to and category user has chosen.
        link_name (str): Name of link user has chosen.

    """
    node, link_category = node_details
    link = nuke.createNode(LINK_NODE_TYPE)
    add_node_link_tab(link)

    tile_color = get_tile_color(node, link_category)
    link.knob('hide_input').setValue(True)
    link['tile_color'].setValue(tile_color)
    link['label'].setValue('NodeLink\n{}: {}'.format(link_category, link_name))

    add_buttons(link)
    add_linked_node_details(link, link_category, link_name)

    link.setInput(0, node)


def add_linked_node_details(node, link_category, link_name):
    """Add custom knob containing link details.

    Args:
        node (nuke.Node): Linked Node to add information to.
        link_category (str): Category of link.
        link_name (str): Link name.

    """
    knob_name = KNOB_NAMES['Linked']
    knob = nuke.Text_Knob(knob_name, link_category, link_name)
    knob.setVisible(False)
    node.addKnob(knob)


def get_tile_color(node, link_category):
    """Retrieve value of tile_color knob converted into hexadecimal.

    Args:
        node (nuke.Node): Node to get the color from.
        link_category (str): Category of Link.

    Returns:
        Color as hexadecimal values.

    """
    if not node['tile_color'].value():
        red, green, blue, alpha = COLORS[link_category]
        tile_color = int('%02x%02x%02x%02x' % (red*255,
                                               green*255,
                                               blue*255,
                                               1),
                         16)
    else:
        tile_color = node['tile_color'].value()

    return tile_color


def add_buttons(link):
    """"Add custom buttons to given node.

    Args:
        link (nuke.Node): Node to add custom knobs.

    """
    jump_to_input_node = ('from nuke_node_linker import model;'
                          'model.jump_to_node(nuke.thisNode().input(0))')

    node_open = 'nuke.show(nuke.thisNode().input(0))'

    link_duplicate = ('from nuke_node_linker import model;'
                      'model.duplicate_link(nuke.thisNode())')

    label = '<font size="3" color="orange">  {}  </font>'

    jump_knob = nuke.PyScript_Knob('jump',
                                   label.format('jump to source'),
                                   jump_to_input_node)

    open_knob = nuke.PyScript_Knob('open_properties',
                                   label.format('open link properties'),
                                   node_open)

    duplicate_linked_node = nuke.PyScript_Knob('duplicate_link',
                                               label.format('duplicate link'),
                                               link_duplicate)
    link.addKnob(jump_knob)
    link.addKnob(open_knob)
    link.addKnob(duplicate_linked_node)


def jump_to_node(node):
    """Change DAG posotion to nodes X and Y position.

    Args:
        node (nuke.Node): Node to jump to.

    """
    nuke.zoom(2, [node.xpos(), node.ypos()])


def duplicate_link(node):
    """Copy and paste an already created link.

    Args:
        node (nuke.Node): Node to copy.

    """
    selection = nuke.selectedNodes()
    nukescripts.clear_selection_recursive()
    node.setSelected(True)
    nukescripts.node_copypaste()
    duplicate = nuke.selectedNode()
    duplicate.setXYpos(node.xpos() + 100, node.ypos())
    duplicate.setInput(0, node.input(0))
    duplicate.setSelected(False)
    for node_ in selection:
        node_.setSelected(True)


def reconnect_links():
    """Connect inputs based on knob values. """
    links = get_all_linked_nodes('Link')
    for node in nuke.selectedNodes():
        if sanity_check(node, KNOB_NAMES['Linked']):
            return
        knob = node[KNOB_NAMES['Linked']]
        link_category = knob.label()
        link_name = knob.value()

        if link_name in links and links[link_name][1] == link_category:
            node.setInput(0, links[link_name][0])
