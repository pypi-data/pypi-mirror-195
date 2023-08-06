
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class console:
    def __init__(self):
        print("Loaded")
    def warn(text):
        print(color.WARNING + "WARN: " + text)
    def error(text):
        print(color.FAIL + "ERROR: " + text)
    def info(text):
        print(color.OKBLUE + "INFO: " + text)


class returns:
    def OKBLUE(text):
        return color.OKBLUE + text
    def OKCYAN(text):
        return color.OKCYAN + text
    def OKGREEN(text):
        return color.OKGREEN + text
    def OKYELLOW(text):
        return color.WARNING + text
    def OKRED(text):
        return color.FAIL + text


class type_texts:
    def BOLD(text):
        return color.BOLD + text
    def UNDERLINE(text):
        return color.UNDERLINE + text

