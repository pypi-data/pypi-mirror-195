import numpy as np

def create_points(depth):
    h, w = depth.shape
    theta, phi = np.mgrid[0:np.pi:h*1j,0:2*np.pi:w*1j]
    x = depth * np.sin(theta) * np.cos(phi)
    y = depth * np.sin(theta) * np.sin(phi)
    z = depth * np.cos(theta)
    return np.dstack((x, y, z)).reshape((-1, 3)).astype('float32')

def create_triangles(points):
    h, w = points.shape[:2]
    i, j = np.mgrid[:h,:w]
    idx = i * w + j
    tri_up = np.dstack((idx[:-1,:], np.roll(idx[:-1,:], -1, axis=1), idx[1:])).reshape((-1, 3))
    tri_down = np.dstack((np.roll(idx[:-1,:], -1, axis=1), np.roll(idx[1:,:], -1, axis=1), idx[1:])).reshape((-1, 3))
    return np.concatenate((tri_up, tri_down), axis=0).astype('uint32')