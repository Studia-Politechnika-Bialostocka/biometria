import cv2


def filter_image(image_path, pixel_size, filter_type):
    pixel_size = int(pixel_size)
    if filter_type == 'Pixelization':
        return pixelization(image_path, pixel_size)
    elif filter_type == 'Median Filter':
        return median_filter(image_path, pixel_size)
    elif filter_type == 'Kuwahara Filter':
        return kuwahara_filter(image_path, pixel_size)
    elif filter_type == 'Gaussian Filter':
        return gaussian_filter(image_path, pixel_size)
    elif filter_type == 'Sobel Filter':
        return sobel_filter(image_path, pixel_size)


def gaussian_filter(image_path, pixel_size):
    pass


def sobel_filter(image_path, pixel_size):
    pass


def kuwahara_filter(image_path, pixel_size):
    pass


def pixelization(image_path, pixel_size):
    tmp = cv2.imread(image_path)
    blue, green, red = cv2.split(tmp)
    height, width = blue.shape
    for x in range(0, width, pixel_size):
        for y in range(0, height, pixel_size):
            endX = x + pixel_size
            endY = y + pixel_size
            if endX > width:
                endX = width
            if endY > height:
                endY = height
            blue[x:endX, y:endY] = blue[x:x + pixel_size, y: y + pixel_size].mean()
            green[x:endX, y:endY] = green[x:x + pixel_size, y: y + pixel_size].mean()
            red[x:endX, y:endY] = red[x:x + pixel_size, y: y + pixel_size].mean()
    output = cv2.merge((blue, green, red))
    return output


def median_filter(image_path, pixel_size):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    temp = []
    indexer = pixel_size // 2
    window = [  # offsety pikseli
        (i, j)
        for i in range(-indexer, pixel_size - indexer)
        for j in range(-indexer, pixel_size - indexer)
    ]
    index = len(window) // 2
    for i in range(len(image)):
        for j in range(len(image[0])):
            image[i][j] = sorted(
                0 if (  # 0 jeżeli i + offset lub j + offset wychodza poza obraz
                        min(i + a, j + b) < 0
                        or len(image) <= i + a
                        or len(image[0]) <= j + b
                ) else image[i + a][j + b]
                for a, b in window
            )[index]
    return image
