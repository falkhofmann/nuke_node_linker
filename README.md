
Usage
-----
In the time where there have been a lot of hidden input tools are floating around, I build up my own since each of them were missing feature I would like to have as well as had bigger performance impact.

To see the tool in action, check out the [demo](https://vimeo.com/301644105) on vimeo.

Install
-------
Make sure outer nuke_node_linker folder is your nuke nuke.pluginPath
Add some variation of the following lines to your menu.py.


    from nuke_node_linker import controller_create_link, controller_add_link
    from nuke_node_linker import model as node_linker_model

    menu = nuke.menu('Nodes').addMenu("custom")
    menu.addCommand("Node Linker/NodeLinker add Link", "controller_add_link.start()", "ctrl+shift+tab")
    menu.addCommand("Node Linker/NodeLinker get Link", "controller_create_link.start()", "shift+tab")
    menu.addCommand("Node Linker/NodeLinker reconnect", "node_linker_model.reconnect_links()")
