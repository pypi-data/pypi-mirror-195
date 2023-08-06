import cognite.client as cl

def hello(string): 
    return "Hello %s!" % (string)

def versionCheck():
    return "Version : " + cl.__version__