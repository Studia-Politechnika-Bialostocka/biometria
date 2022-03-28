import cv2


def pixelate_image(image, pixel_size):
    tmp = image
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
            blue[x:endX, y:endY] = blue[x:x+pixel_size, y: y+pixel_size].mean()
            green[x:endX, y:endY] = green[x:x + pixel_size, y: y + pixel_size].mean()
            red[x:endX, y:endY] = red[x:x + pixel_size, y: y + pixel_size].mean()
    output = cv2.merge((blue, green, red))
    return output