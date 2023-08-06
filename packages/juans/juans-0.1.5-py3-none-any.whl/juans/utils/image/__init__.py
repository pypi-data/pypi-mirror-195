"""
 Author: yican.yc
 Date: 2022-08-23 19:24:05
 Last Modified by:   yican.yc
 Last Modified time: 2022-08-23 19:24:05
"""
import base64
from io import BytesIO
from pathlib import Path

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests
from PIL import Image


def image_to_base64_bytes(image_path):
    with open(image_path, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
    return encoded_bytes


def image_to_base64_string(image_path, encoding="ascii"):
    return image_to_base64_bytes(image_path).decode(encoding)


def base64_bytes_to_numpy(encoded_bytes):
    return np.array(Image.open(BytesIO(base64.b64decode(encoded_bytes))).convert("RGB"))


def base64_string_to_numpy(base64_string, encoding="ascii"):
    return base64_bytes_to_numpy(base64_string.encode(encoding))


def read_image(image_path):
    """读取图像数据, 转换为RGB格式, 最终转换为numpy array
    image_path: 可以为网络url, 本地path, bytes
    return: numpy array
    """
    if isinstance(image_path, bytes):
        return np.array(Image.open(BytesIO(image_path)).convert(mode="RGB"))
    try:
        return np.array(Image.open(image_path).convert(mode="RGB"))
        # return cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    except Exception:
        return np.array(Image.open(requests.get(image_path, stream=True).raw).convert(mode="RGB"))


def show_image(image_path, title=None, fig_size=(10, 5), font_size=12, ax=None):
    """展示单幅图
    font_size -> https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot

    Parameters
    ----------
    image_path : str
        图像路径
    title : str, optional
        图像标题, by default None
    fig_size : tuple, optional
        图像大小, by default (10, 5)
    font_size : int, optional
        字体大小, by default 12
    ax : matplotlib.axes._subplots.AxesSubplot, optional
        , by default None

    Examples
    --------
        show_image(image_path="your_image_path")
    """

    matplotlib.rc("font", **{"size": font_size})

    if ax is not None:
        ax.set_title(title)
        ax.imshow(read_image(image_path))
    else:
        plt.figure(figsize=fig_size)
        plt.title(title)
        plt.imshow(read_image(image_path))


def show_images(image_paths, titles=[], n_cols=3, fig_width=16, font_size=12, height_ratio=1.05):
    """以网格的形式展示多幅图

    Parameters
    ----------
    image_paths : [type]
        图像路径
    titles : list, optional
        图像标题, by default []
    n_cols : int, optional
        列数, by default 3
    fig_width : int, optional
        图像宽度, 高度会被自动计算，, by default 16
    font_size : int, optional
        字体大小, by default 12

    Examples
    --------
        show_image(image_path=["your_image_path", "your_image_path"], titles=["title", "title"])
    """

    matplotlib.rc("font", **{"size": font_size})

    # 计算子图的行列
    n_images = len(image_paths)
    n_rows = n_images // n_cols
    n_rows = n_rows if (n_images % n_cols == 0) else (n_rows + 1)
    img = read_image(image_paths[0])
    w_h_ratio = img.shape[1] / img.shape[0]
    fig_size = (fig_width, (fig_width * n_rows) / (n_cols * w_h_ratio) * height_ratio)

    # 补全标题
    titles = titles + [None] * (n_images - len(titles))

    # 生成所有子图的区域
    fig, ax = plt.subplots(n_rows, n_cols, figsize=fig_size)
    ax = ax.flatten()

    for i, image_path in enumerate(image_paths):
        show_image(image_path=image_path, ax=ax[i], title=titles[i], font_size=font_size)


def show_images_under_folder(folder_path, num_of_pictures, n_cols=3, fig_width=16, font_size=12, height_ratio=1.6):
    """
    展示某个folder下的图片
    """
    p = Path(folder_path)
    image_paths = list(p.iterdir())
    sample_image_paths = image_paths[:num_of_pictures]
    print(f"total images : {len(image_paths)}")
    show_images(
        sample_image_paths,
        titles=[str(i).split("/")[-1] for i in sample_image_paths],
        n_cols=3,
        fig_width=16,
        font_size=12,
        height_ratio=height_ratio,
    )
