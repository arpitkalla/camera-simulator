import cv2 
import math
import numpy as np
import matplotlib.pyplot as plt


width, height = 200, 100

roll, pitch, yaw = 0.0 * np.pi / 180, 30.0 * np.pi / 180, 0.0 * np.pi / 180

x, y, z = 600.0, 500.0, 500.0

# Calculates Rotation Matrix given euler angles.
def eulerAnglesToRotationMatrix(theta) :

    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
              
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])

    R = np.dot(np.dot(R_z, R_x), R_y)
    return R

def get_points(x, y, z, roll, pitch, yaw, width, height):
	points = []
	theta = np.asarray([roll, pitch, yaw])
	pos = np.array([x,y,z])
	R = eulerAnglesToRotationMatrix(theta)
	v_init = np.array([0,0,-1])
	# v = np.dot(R, v_init.T).T
	for i in [[1,-1], [1,1], [-1,1], [-1,-1]]:
		t = [i[0]*width/2 , i[1]*height/2 , 0]
		t = t / np.linalg.norm(t)
		v_f = R.dot(v_init + t)
		v_f = v_f / np.linalg.norm(v_f)
		point = (-pos[2]/v_f[2] * v_f)[:2] + pos[:2]
		points.append(point)
	return np.asarray(points)


im = cv2.imread("test.png")

print(im.shape)

# pts = np.array([[250, 295],
# 				[220, 700],
# 				[550, 400],
# 				[620, 900]])

pts = get_points(x, y, z, roll, pitch, yaw, width, height)
print(pts)
# width, height = 200, 100
pts2 = np.array([[width,0],[width,height], [0,height], [0,0]]) 

plt.imshow(im)
plt.plot(pts[:,0], pts[:,1], "-")
plt.plot(pts[0,0], pts[0,1], "ro")
# plt.plot(pts[1,0], pts[1,1], "bo")
plt.plot(pts[3,0], pts[3,1], "go")
plt.show()
h, status = cv2.findHomography(pts, pts2)

im2 = cv2.warpPerspective(im, h, (width, height))
plt.imshow(im2)
plt.show() 