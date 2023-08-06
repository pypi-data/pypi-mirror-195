import matplotlib.pyplot as plt
import numpy as np


def info():
    print('The version number of Ddnet is 0.0.3! This project is not very useful! ')


def draw_features(width, height, x, savename, gray=False, dpi=100):
    fig = plt.figure(figsize=(16, 16))
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.05, hspace=0.05)
    for i in range(width * height):
        plt.subplot(height, width, i + 1)
        plt.axis('off')
        img = x[0, i, :, :]
        pmin = np.min(img)
        pmax = np.max(img)
        img = (img - pmin) / (pmax - pmin + 0.000001)
        if gray:
            plt.imshow(img, cmap='gray')
        plt.imshow(img)
        print("{}/{}".format(i, width * height))
    fig.savefig(savename, dpi=dpi)
    fig.clf()
    plt.close()
