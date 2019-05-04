
# Main types of marks
CATEGORIES = ['Bookmark', 'Link']

# Name of tab on node
TAB_NAME = 'NodeLinks'

# Define specific knob names to create and access
KNOB_NAMES = {'Link': 'node_link',
              'Linked': 'linked_node',
              'Bookmark': 'node_bookmark'}

# Define node type to create as linked node
LINK_NODE_TYPE = 'NoOp'

# default color of linked node
LINKED_NODE_DEFAULT_COLOR = 506285055

# Widget colors for main types
WIDGET_COLORS = {'Bookmark': (0.5, 0.8, 0.9),
                 'Link': (0.2, 0.3, 0.9)}

# Specify colors for certain types
# Should be rather in a yaml file than in here
COLORS = {'Camera': (0.31, 0.03, 0.03, 0.75),
          'CGFX': (0.3, 0.7, 0.0, 0.75),
          'DMP': (0.7, 0.3, 0.0, 0.75),
          'Element': (0.25, 0.25, 0.25, 0.75),
          'Lighting': (0.28, 0.42, 0.53, 0.75),
          'Plate': (0.1, 0.27, 0.13, 0.75),
          'Roto': (0.45, 0.18, 0.39, 0.75),
          '-------': (0.3, 0.2, 0.5, 0.75)
          }

# Regular expression for link names
NAME_REGEX = '[a-zA-Z_]+'
