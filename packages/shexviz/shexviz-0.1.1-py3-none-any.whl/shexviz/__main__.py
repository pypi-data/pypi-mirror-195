import sys
from shexviz import shex2dot

def main():
    if len(sys.argv) > 1:
        shex2dot.main(sys.argv[1:])
    else:
        print("Usage: shexviz <shexfile>")

if __name__ == "__main__":
    main()

