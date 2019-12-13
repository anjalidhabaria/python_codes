import tf.transformations as tft
import numpy as np
mat = tft.quaternion_matrix([0, 0, 0, 1])
array([[ 1.,  0.,  0.,  0.],
       [ 0.,  1.,  0.,  0.],
       [ 0.,  0.,  1.,  0.],
       [ 0.,  0.,  0.,  1.]])
mat[:3, :3]
array([[ 1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0.,  1.]])
tft.quaternion_from_matrix(mat)
array([ 0.,  0.,  0.,  1.])
mat2 = np.array([[0.866, -0.5,   0, 0],
                     [0.5,    0.866, 0, 0],
                     [0,      0,     1, 0],
                     [0,      0,     0, 1]])
tft.quaternion_from_matrix(mat2)
array([ 0.        ,  0.        ,  0.25882081,  0.96591925])
from geometry_msgs.msg import Quaternion
yaw_by_30 = Quaternion(x=0, y=0, z=0.25882081, w=0.96591925)
