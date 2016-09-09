import math


class Quaternion(object):
    """
    Quaternion class for quaternion operations and 3D rotations.
    """
    def __init__(self, input):
        self.w = input[0]
        self.x = input[1]
        self.y = input[2]
        self.z = input[3]

    def __repr__(self):
        return "<Quaternion object w:%s x:%s y:%s z:%s>" % (self.w, self.x, self.y, self.z)

    def __str__(self):
        return "x:%s y:%s z:%s" % (self.x, self.y, self.z)

    def xyz(self):
        """
        Returns x, y, z values of the quaternion in list format.
        """
        return [self.x, self.y, self.z]

    def __mul__(self, quat2):
        """
        Multiply quaternion by another.

        Example usage::
          >>> q1 = Quaternion([1, 2, 3, 4])
          >>> q2 = Quaternion([2, 3, 4, 5])
          >>> q1 * q2 -> <Quaternion object w:-36 x:6 y:12 z:12>
        """

        q1 = self
        q2 = quat2

        w3 = q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
        x3 = q1.x * q2.w + q1.w * q2.x - q1.z * q2.y + q1.y * q2.z
        y3 = q1.y * q2.w + q1.z * q2.x + q1.w * q2.y - q1.x * q2.z
        z3 = q1.z * q2.w - q1.y * q2.x + q1.x * q2.y + q1.w * q2.z

        return Quaternion([w3, x3, y3, z3])

    def __truediv__(self, quat2):
        """
        Divide one quaternion by another. Performs the operation as q1 * inverse q2.

        Example usage::
          >>> q1 = Quaternion([1, 2, 3, 4])
          >>> q2 = Quaternion([2, 3, 4, 5])
          >>> q1 / q2 -> <Quaternion object w:0.7407 x:0.0370 y:0.0 z:0.0741>
        """
        return self * quat2.inv()

    def inv(self):
        """
        Returns the inverse of the quaternion as a new quaternion.

        """
        norm = self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2

        return Quaternion([self.w / norm, -self.x / norm, -self.y / norm, -self.z / norm])

    def rotation(self, rotation_point, axis_point1, axis_point2, rotation_angle):
        """
        Rotation of a point around an axis defined by two points in 3D space.
        Rotation angle needs to be given in radians.

        Example usage::
         >>> Q = Quaternion([0, 1, 1, 1])
         >>> Q = Q.rotation(Q.xyz(), [-2, 4, 6.1], [0.3, 1.2, -0.76], math.pi/6)
         >>> [2.1192250600275795, 2.2773560513200133, 5.890236840657188]
        """
        i = axis_point2[0] - axis_point1[0]
        j = axis_point2[1] - axis_point1[1]
        k = axis_point2[2] - axis_point1[2]
        length = math.sqrt(i**2 + j**2 + k**2)
        i = i / length
        j = j / length
        k = k / length
        qp_w = 0
        qp_x = rotation_point[0] - axis_point2[0]
        qp_y = rotation_point[1] - axis_point2[1]
        qp_z = rotation_point[2] - axis_point2[2]
        Q_point = Quaternion([qp_w, qp_x, qp_y, qp_z])

        qr_w = math.cos(rotation_angle / 2.0)
        qr_x = math.sin(rotation_angle / 2.0) * i
        qr_y = math.sin(rotation_angle / 2.0) * j
        qr_z = math.sin(rotation_angle / 2.0) * k
        Q_rot = Quaternion([qr_w, qr_x, qr_y, qr_z])

        Quat = (Q_rot * Q_point) * Q_rot.inv()
        Quat.x = Quat.x + axis_point2[0]
        Quat.y = Quat.y + axis_point2[1]
        Quat.z = Quat.z + axis_point2[2]

        return Quat

    def coor(self):
        """
        Converts Quaternion object to Coor object.
        """
        from moleidoscope.geometry.coor import Coor as Coor
        return Coor(self.xyz())
