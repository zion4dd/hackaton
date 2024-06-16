def dist(a, b):
    return abs(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** (1 / 2))

a, b = (1, 1), (3, 3)
print(dist(a, b))



# import numpy as np
# def sample():
#     w, h = 512, 512
#     data = np.zeros((h, w, 3), dtype=np.uint8)
#     data[0:256, 0:256] = [255, 0, 0] # red patch in upper left
#     img = Image.fromarray(data)
#     filepath = current_directory + f"\\frames\\frame_{str(int(time()))}.png"
#     img.save(filepath)
#     return filepath

