# stdlib
import os

# third party
import click
import matplotlib.pyplot as plt


def readlines(path):
    with open(path, "r") as handle:
        return handle.read().splitlines()


def process(files):
    return [[len(line) for line in lines if len(line) != 0] for lines in files]


def unpack(lists):
    return [val for lst in lists for val in lst]


def getpaths(directory, extensions=[".py"]):

    return [
        os.path.join(r, file)
        for r, d, f in os.walk(directory)
        for file in f
        if os.path.splitext(file)[1] in extensions
    ]


def plot(values):
    plt.hist(values, bins=100)
    plt.show()

@click.command()
@click.argument('directory')
def main(directory="."):
    plot(unpack(process(map(readlines, getpaths(directory)))))


if __name__=='__main__':
    main()
    
