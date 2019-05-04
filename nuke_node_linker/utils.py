# Import built-in modules
import os


def set_style_sheet(widget):

    style_sheet = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                "stylesheet.css"))

    with open(style_sheet, "r") as file_:
        style = file_.read()
        widget.setStyleSheet(style)


def get_icon_path(category):
    return os.path.normpath(os.path.join(os.path.dirname(__file__),
                                         "icons",
                                         "{}.png".format(category)))
