import numpy as np
from filterpy.kalman import KalmanFilter

class BallKalman:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=4, dim_z=2)
        self.kf.x = np.zeros((4,1))
        self.kf.F = np.array([[1,0,1,0],
                              [0,1,0,1],
                              [0,0,1,0],
                              [0,0,0,1]], dtype=float)
        self.kf.H = np.array([[1,0,0,0],
                              [0,1,0,0]], dtype=float)
        self.kf.P *= 1000
        self.kf.R *= 5

    def update(self, detection):
        if detection is not None:
            z = np.array([[detection[0]], [detection[1]]])
            self.kf.update(z)
        else:
            self.kf.predict()

        return self.kf.x[:2].reshape(-1)
