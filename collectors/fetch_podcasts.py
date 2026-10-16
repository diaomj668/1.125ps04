from common import *
from feed_support import collect
def main(): collect(runarg(),"podcast")
if __name__=="__main__": cli(main)
