from time import ctime

from telegraph2star import __version__


def run():
    cur_time = ctime()
    text = f"""
    # telegraph2star
    
    version {__version__} ({cur_time} +0800)
    """
    print(text)
