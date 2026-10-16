from common import *
from feed_support import collect
def main(): collect(runarg(),"feed")
if __name__=="__main__": cli(main)
