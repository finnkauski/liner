# stdlib
import os

# third party
import matplotlib.pyplot as plt

path = "."
result = [os.path.join(r, file) for r, d, f in os.walk(path) for file in f]
print(result)
