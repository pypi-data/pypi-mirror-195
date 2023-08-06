from time import ctime

from telegraph4j import __version__


def run():
    cur_time = ctime()
    text = f"""
    # telegraph4j
    
    version {__version__} ({cur_time} +0800)
    """
    print(text)
