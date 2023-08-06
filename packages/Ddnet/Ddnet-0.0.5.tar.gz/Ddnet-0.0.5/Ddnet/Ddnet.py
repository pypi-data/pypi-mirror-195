import matplotlib.pyplot as plt
import numpy as np
import random
import os


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


def data_split(full_list, ratio, shuffle=True):
    n_total = len(full_list)
    offset = int(n_total * ratio)
    if n_total == 0 or offset < 1:
        return [], full_list
    if shuffle:
        random.shuffle(full_list)
    sublist_1 = full_list[:offset]
    sublist_2 = full_list[offset:]
    return sublist_1, sublist_2


def rename_file_tree(path):
    # Get the list of files in the current directory
    file_list = os.listdir(path)
    # print(file_list)
    global file_count, folder_count

    # Traverse the file list. If the current file is not a folder, the number of files+1. If it is a folder, the number of folders+1 and then call the method of counting the number of files
    for i in file_list:
        path_now = path + "\\" + i
        print(path_now)
        if os.path.isdir(path_now) == True:
            print(path_now, path)
            folder_count = folder_count + 1
            rename_file_tree(path_now)
        else:
            file_count = file_count + 1
            #            print(path_now)
            os.rename(path_now, os.path.abspath(path + '/' + 's' + str(file_count) + '.png'))

    return file_count
