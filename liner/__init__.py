# stdlib
import os

# third party
import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# constants


def readlines(path):
    with open(path, "r") as handle:
        return handle.read().splitlines()


def process(files):
    return [[len(line) for line in lines if len(line) != 0] for lines in files]


def group(lists):
    series = pd.Series([val for lst in lists for val in lst])
    bin_n = int(len(series.unique()) // len(series.unique()) ** (1 / 2))

    bins = pd.cut(series, bin_n)
    print(f"Created {bin_n} bins")
    return series.groupby(bins).mean().sort_values(ascending=False)


def getpaths(directory, extensions):

    return [
        os.path.join(r, file)
        for r, d, f in os.walk(directory)
        for file in f
        if os.path.splitext(file)[1] in extensions
    ]


def plot(values):
    def plt_circle(ax, r, maximum, color):
        plot = lambda: ax.add_artist(plt.Circle((0, r - maximum), r, color=color))
        if r < maximum * 0.5:
            plot()
        else:
            ax.add_artist(plt.Circle((0, r - maximum), r * 1.03, color="#ffffff"))
            plot()

    def gen_color(i, r, maximum, l):
        return (min(1, i / l * 1.5), min(1, (i / l)), min(1, (i / l) * 0.9))

    # matplotlib
    fig, ax = plt.subplots(1)
    mx = max(values)
    l = len(values)
    limits = mx * 1.1
    plt.xlim(-limits, limits)
    plt.ylim(-limits, limits)
    ax.set_aspect(1)

    # Can do with arrays instead
    # plotting
    for (i, r) in enumerate(values):
        color = gen_color(i, r, mx, l)
        plt_circle(ax, r, mx, color)

    plt.grid(False)
    plt.show()


@click.command()
@click.argument("extensions", nargs=-1)
@click.argument("directory", required=True)
def main(extensions, directory="."):
    if not extensions:
        extensions = [".py"]

    print(f"Working with the following extensions: {extensions}")

    plot(group(process(map(readlines, getpaths(directory, extensions)))))


if __name__ == "__main__":
    main()
