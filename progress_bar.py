import sys

def progressbar(i, count, prefix="", size=60, file=sys.stdout):
    # count = len(it)
    x = int(size*i/count)
    file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), i, count))
    file.flush()

if __name__ == '__main__':
    import time
    progressbar(3, 5, "Computing: ")
    progressbar(3, 5, "Computing: ")
    sys.stdout.write("\n")
    sys.stdout.flush()