def enableScrolling(enable):
    doc().body.style.setProperty("overflow", enable and 'auto' or 'hidden', '')

def setMargin(size):
    doc().body.style.setProperty("margin", size, '')

def prompt(msg, defaultReply=""):
    return wnd().prompt(msg, defaultReply)


