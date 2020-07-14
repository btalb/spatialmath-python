import numpy.testing as nt
import matplotlib.pyplot as plt
import unittest

"""
we will assume that the primitives rotx,trotx, etc. all work
"""
from math import pi
from spatialmath.pose3d import *
from spatialmath import super_pose as sp
from spatialmath.base import *
from spatialmath.base import argcheck


def array_compare(x, y):
    if isinstance(x, sp.SMPose):
        x = x.A
    if isinstance(y, sp.SMPose):
        y = y.A
    if isinstance(x, sp.SMTwist):
        x = x.S
    if isinstance(y, sp.SMTwist):
        y = y.S
    nt.assert_array_almost_equal(x, y)


class TestSO3(unittest.TestCase):

    def test_constructor(self):

        # null constructor
        R = SO3()
        nt.assert_equal(len(R), 1)
        array_compare(R, np.eye(3))
        self.assertIsInstance(R, SO3)

        # empty constructor
        R = SO3.Empty()
        nt.assert_equal(len(R), 0)
        self.assertIsInstance(R, SO3)

        # construct from matrix
        R = SO3(rotx(0.2))
        nt.assert_equal(len(R), 1)
        array_compare(R, rotx(0.2))
        self.assertIsInstance(R, SO3)

        # construct from canonic rotation
        R = SO3.Rx(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, rotx(0.2))
        self.assertIsInstance(R, SO3)

        R = SO3.Ry(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, roty(0.2))
        self.assertIsInstance(R, SO3)

        R = SO3.Rz(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, rotz(0.2))
        self.assertIsInstance(R, SO3)

        # triple angle
        R = SO3.Eul([0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, eul2r([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SO3)

        R = SO3.Eul(np.r_[0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, eul2r([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SO3)

        R = SO3.Eul([10, 20, 30], unit='deg')
        nt.assert_equal(len(R), 1)
        array_compare(R, eul2r([10, 20, 30], unit='deg'))
        self.assertIsInstance(R, SO3)

        R = SO3.RPY([0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2r([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SO3)

        R = SO3.RPY(np.r_[0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2r([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SO3)

        R = SO3.RPY([10, 20, 30], unit='deg')
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2r([10, 20, 30], unit='deg'))
        self.assertIsInstance(R, SO3)

        R = SO3.RPY([0.1, 0.2, 0.3], order='xyz')
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2r([0.1, 0.2, 0.3], order='xyz'))
        self.assertIsInstance(R, SO3)

        # angvec
        R = SO3.AngVec(0.2, [1, 0, 0])
        nt.assert_equal(len(R), 1)
        array_compare(R, rotx(0.2))
        self.assertIsInstance(R, SO3)

        R = SO3.AngVec(0.3, [0, 1, 0])
        nt.assert_equal(len(R), 1)
        array_compare(R, roty(0.3))
        self.assertIsInstance(R, SO3)

        # OA
        R = SO3.OA([0, 1, 0], [0, 0, 1])
        nt.assert_equal(len(R), 1)
        array_compare(R, np.eye(3))
        self.assertIsInstance(R, SO3)

        # random
        R = SO3.Rand()
        nt.assert_equal(len(R), 1)
        self.assertIsInstance(R, SO3)

        # copy constructor
        R = SO3.Rx(pi / 2)
        R2 = SO3(R)
        R = SO3.Ry(pi / 2)
        array_compare(R2, rotx(pi / 2))

    def test_about(self):
        R = SO3()
        R.about()

    def test_display(self):
        R = SO3()

        s = str(R)
        self.assertIsInstance(s, str)
        self.assertEqual(s.count('\n'), 3)

        s = repr(R)
        self.assertIsInstance(s, str)
        self.assertEqual(s.count('\n'), 3)

        R.print()

        R.printline()

    def test_listpowers(self):
        R = SO3()
        R1 = SO3.Rx(0.2)
        R2 = SO3.Ry(0.3)

        R.append(R1)
        R.append(R2)
        nt.assert_equal(len(R), 3)
        self.assertIsInstance(R, SO3)

        array_compare(R[0], np.eye(3))
        array_compare(R[1], R1)
        array_compare(R[2], R2)

        R = SO3([rotx(0.1), rotx(0.2), rotx(0.3)])
        nt.assert_equal(len(R), 3)
        self.assertIsInstance(R, SO3)
        array_compare(R[0], rotx(0.1))
        array_compare(R[1], rotx(0.2))
        array_compare(R[2], rotx(0.3))

        R = SO3([SO3.Rx(0.1), SO3.Rx(0.2), SO3.Rx(0.3)])
        nt.assert_equal(len(R), 3)
        self.assertIsInstance(R, SO3)
        array_compare(R[0], rotx(0.1))
        array_compare(R[1], rotx(0.2))
        array_compare(R[2], rotx(0.3))

    def test_tests(self):

        R = SO3()

        self.assertEqual(R.isrot(), True)
        self.assertEqual(R.isrot2(), False)
        self.assertEqual(R.ishom(), False)
        self.assertEqual(R.ishom2(), False)

    def test_properties(self):

        R = SO3()

        self.assertEqual(R.isSO, True)
        self.assertEqual(R.isSE, False)

        array_compare(R.n, np.r_[1, 0, 0])
        array_compare(R.n, np.r_[1, 0, 0])
        array_compare(R.n, np.r_[1, 0, 0])

        nt.assert_equal(R.N, 3)
        nt.assert_equal(R.shape, (3, 3))

        R = SO3.Rx(0.3)
        array_compare(R.inv * R, np.eye(3, 3))

    def test_arith(self):
        R = SO3()

        # sum
        a = R + R
        self.assertNotIsInstance(a, SO3)
        array_compare(a, np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]]))

        a = R + 1
        self.assertNotIsInstance(a, SO3)
        array_compare(a, np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]]))

        # a = 1 + R
        # self.assertNotIsInstance(a, SO3)
        # array_compare(a, np.array([ [2,1,1], [1,2,1], [1,1,2]]))

        a = R + np.eye(3)
        self.assertNotIsInstance(a, SO3)
        array_compare(a, np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]]))

        # a =  np.eye(3) + R
        # self.assertNotIsInstance(a, SO3)
        # array_compare(a, np.array([ [2,0,0], [0,2,0], [0,0,2]]))
        #  this invokes the __add__ method for numpy

        R += R
        self.assertNotIsInstance(a, SO3)
        array_compare(a, np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]]))

        R = SO3()
        R += 1
        self.assertNotIsInstance(R, SO3)
        array_compare(R, np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]]))

        # difference
        R = SO3()

        a = R - R
        self.assertNotIsInstance(a, SO3)
        array_compare(a, np.zeros((3, 3)))

        a = R - 1
        self.assertNotIsInstance(a, SO3)
        array_compare(a, np.array([[0, -1, -1], [-1, 0, -1], [-1, -1, 0]]))

        # a = 1 - R
        # self.assertNotIsInstance(a, SO3)
        # array_compare(a, -np.array([ [0,-1,-1], [-1,0,-1], [-1,-1,0]]))

        a = R - np.eye(3)
        self.assertNotIsInstance(a, SO3)
        array_compare(a, np.zeros((3, 3)))

        # a =  np.eye(3) - R
        # self.assertNotIsInstance(a, SO3)
        # array_compare(a, np.zeros((3,3)))

        R -= R
        self.assertNotIsInstance(R, SO3)
        array_compare(R, np.zeros((3, 3)))

        R = SO3()
        R -= 1
        self.assertNotIsInstance(R, SO3)
        array_compare(R, np.array([[0, -1, -1], [-1, 0, -1], [-1, -1, 0]]))

        # multiply
        R = SO3()

        a = R * R
        self.assertIsInstance(a, SO3)
        array_compare(a, R)

        a = R * 2
        self.assertNotIsInstance(a, SO3)
        array_compare(a, 2 * np.eye(3))

        a = 2 * R
        self.assertNotIsInstance(a, SO3)
        array_compare(a, 2 * np.eye(3))

        R = SO3()
        R *= SO3.Rx(pi / 2)
        self.assertIsInstance(R, SO3)
        array_compare(R, rotx(pi / 2))

        R = SO3()
        R *= 2
        self.assertNotIsInstance(R, SO3)
        array_compare(R, 2 * np.eye(3))

        array_compare(SO3.Rx(pi / 2) * SO3.Ry(pi / 2) * SO3.Rx(-pi / 2), SO3.Rz(pi / 2))

        array_compare(SO3.Ry(pi / 2) * [1, 0, 0], np.c_[0, 0, -1].T)

        # SO3 x vector
        vx = np.r_[1, 0, 0]
        vy = np.r_[0, 1, 0]
        vz = np.r_[0, 0, 1]

        def cv(v):
            return np.c_[v]

        nt.assert_equal(isinstance(SO3.Rx(pi / 2) * vx, np.ndarray), True)
        array_compare(SO3.Rx(pi / 2) * vx, cv(vx))
        array_compare(SO3.Rx(pi / 2) * vy, cv(vz))
        array_compare(SO3.Rx(pi / 2) * vz, cv(-vy))

        array_compare(SO3.Ry(pi / 2) * vx, cv(-vz))
        array_compare(SO3.Ry(pi / 2) * vy, cv(vy))
        array_compare(SO3.Ry(pi / 2) * vz, cv(vx))

        array_compare(SO3.Rz(pi / 2) * vx, cv(vy))
        array_compare(SO3.Rz(pi / 2) * vy, cv(-vx))
        array_compare(SO3.Rz(pi / 2) * vz, cv(vz))

        # divide
        R = SO3.Ry(0.3)
        a = R / R
        self.assertIsInstance(a, SO3)
        array_compare(a, np.eye(3))

        a = R / 2
        self.assertNotIsInstance(a, SO3)
        array_compare(a, roty(0.3) / 2)

        # power

        R = SO3.Rx(pi/2)
        R = R**2
        array_compare(R, SO3.Rx(pi))

        R = SO3.Rx(pi/2)
        R **= 2
        array_compare(R, SO3.Rx(pi))

        R = SO3.Rx(pi/4)
        R = R**(-2)
        array_compare(R, SO3.Rx(-pi/2))

        R = SO3.Rx(pi/4)
        R **= -2
        array_compare(R, SO3.Rx(-pi/2))



    def test_arith_vect(self):

        rx = SO3.Rx(pi / 2)
        ry = SO3.Ry(pi / 2)
        rz = SO3.Rz(pi / 2)
        u = SO3()

        # multiply
        R = SO3([rx, ry, rz])
        a = R * rx
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * rx)
        array_compare(a[2], rz * rx)

        a = rx * R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], rx * ry)
        array_compare(a[2], rx * rz)

        a = R * R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * ry)
        array_compare(a[2], rz * rz)

        a = R * 2
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * 2)
        array_compare(a[1], ry * 2)
        array_compare(a[2], rz * 2)

        a = 2 * R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * 2)
        array_compare(a[1], ry * 2)
        array_compare(a[2], rz * 2)

        a = R
        a *= rx
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * rx)
        array_compare(a[2], rz * rx)

        a = rx
        a *= R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], rx * ry)
        array_compare(a[2], rx * rz)

        a = R
        a *= R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * ry)
        array_compare(a[2], rz * rz)

        a = R
        a *= 2
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * 2)
        array_compare(a[1], ry * 2)
        array_compare(a[2], rz * 2)

        # SO3 x vector
        vx = np.r_[1, 0, 0]
        vy = np.r_[0, 1, 0]
        vz = np.r_[0, 0, 1]

        a = R * vx
        array_compare(a[:, 0], (rx * vx).flatten())
        array_compare(a[:, 1], (ry * vx).flatten())
        array_compare(a[:, 2], (rz * vx).flatten())

        a = rx * np.vstack((vx, vy, vz)).T
        array_compare(a[:, 0], (rx * vx).flatten())
        array_compare(a[:, 1], (rx * vy).flatten())
        array_compare(a[:, 2], (rx * vz).flatten())

        # divide
        R = SO3([rx, ry, rz])
        a = R / rx
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], ry / rx)
        array_compare(a[2], rz / rx)

        a = rx / R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], rx / ry)
        array_compare(a[2], rx / rz)

        a = R / R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], np.eye(3))
        array_compare(a[1], np.eye(3))
        array_compare(a[2], np.eye(3))

        a = R / 2
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / 2)
        array_compare(a[1], ry / 2)
        array_compare(a[2], rz / 2)

        a = R
        a /= rx
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], ry / rx)
        array_compare(a[2], rz / rx)

        a = rx
        a /= R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], rx / ry)
        array_compare(a[2], rx / rz)

        a = R
        a /= R
        self.assertIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], np.eye(3))
        array_compare(a[1], np.eye(3))
        array_compare(a[2], np.eye(3))

        a = R
        a /= 2
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / 2)
        array_compare(a[1], ry / 2)
        array_compare(a[2], rz / 2)

        # add
        R = SO3([rx, ry, rz])
        a = R + rx
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + rx)
        array_compare(a[2], rz + rx)

        a = rx + R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], rx + ry)
        array_compare(a[2], rx + rz)

        a = R + R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + ry)
        array_compare(a[2], rz + rz)

        a = R + 1
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + 1)
        array_compare(a[1], ry + 1)
        array_compare(a[2], rz + 1)

        a = R
        a += rx
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + rx)
        array_compare(a[2], rz + rx)

        a = rx
        a += R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], rx + ry)
        array_compare(a[2], rx + rz)

        a = R
        a += R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + ry)
        array_compare(a[2], rz + rz)

        a = R
        a += 1
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + 1)
        array_compare(a[1], ry + 1)
        array_compare(a[2], rz + 1)

        # subtract
        R = SO3([rx, ry, rz])
        a = R - rx
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - rx)
        array_compare(a[2], rz - rx)

        a = rx - R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], rx - ry)
        array_compare(a[2], rx - rz)

        a = R - R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - ry)
        array_compare(a[2], rz - rz)

        a = R - 1
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - 1)
        array_compare(a[1], ry - 1)
        array_compare(a[2], rz - 1)

        a = R
        a -= rx
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - rx)
        array_compare(a[2], rz - rx)

        a = rx
        a -= R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], rx - ry)
        array_compare(a[2], rx - rz)

        a = R
        a -= R
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - ry)
        array_compare(a[2], rz - rz)

        a = R
        a -= 1
        self.assertNotIsInstance(a, SO3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - 1)
        array_compare(a[1], ry - 1)
        array_compare(a[2], rz - 1)

    def test_functions(self):
        # inv
        # .T
        pass

    def test_functions_vect(self):
        # inv
        # .T
        pass


class TestSE3(unittest.TestCase):

    def test_constructor(self):

        # null constructor
        R = SE3()
        nt.assert_equal(len(R), 1)
        array_compare(R, np.eye(4))
        self.assertIsInstance(R, SE3)

        # construct from matrix
        R = SE3(trotx(0.2))
        nt.assert_equal(len(R), 1)
        array_compare(R, trotx(0.2))
        self.assertIsInstance(R, SE3)

        # construct from canonic rotation
        R = SE3.Rx(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, trotx(0.2))
        self.assertIsInstance(R, SE3)

        R = SE3.Ry(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, troty(0.2))
        self.assertIsInstance(R, SE3)

        R = SE3.Rz(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, trotz(0.2))
        self.assertIsInstance(R, SE3)

        # construct from canonic translation
        R = SE3.Tx(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, transl(0.2, 0, 0))
        self.assertIsInstance(R, SE3)

        R = SE3.Ty(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, transl(0, 0.2, 0))
        self.assertIsInstance(R, SE3)

        R = SE3.Tz(0.2)
        nt.assert_equal(len(R), 1)
        array_compare(R, transl(0, 0, 0.2))
        self.assertIsInstance(R, SE3)

        # triple angle
        R = SE3.Eul([0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, eul2tr([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SE3)

        R = SE3.Eul(np.r_[0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, eul2tr([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SE3)

        R = SE3.Eul([10, 20, 30], unit='deg')
        nt.assert_equal(len(R), 1)
        array_compare(R, eul2tr([10, 20, 30], unit='deg'))
        self.assertIsInstance(R, SE3)

        R = SE3.RPY([0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2tr([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SE3)

        R = SE3.RPY(np.r_[0.1, 0.2, 0.3])
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2tr([0.1, 0.2, 0.3]))
        self.assertIsInstance(R, SE3)

        R = SE3.RPY([10, 20, 30], unit='deg')
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2tr([10, 20, 30], unit='deg'))
        self.assertIsInstance(R, SE3)

        R = SE3.RPY([0.1, 0.2, 0.3], order='xyz')
        nt.assert_equal(len(R), 1)
        array_compare(R, rpy2tr([0.1, 0.2, 0.3], order='xyz'))
        self.assertIsInstance(R, SE3)

        # angvec
        R = SE3.AngVec(0.2, [1, 0, 0])
        nt.assert_equal(len(R), 1)
        array_compare(R, trotx(0.2))
        self.assertIsInstance(R, SE3)

        R = SE3.AngVec(0.3, [0, 1, 0])
        nt.assert_equal(len(R), 1)
        array_compare(R, troty(0.3))
        self.assertIsInstance(R, SE3)

        # OA
        R = SE3.OA([0, 1, 0], [0, 0, 1])
        nt.assert_equal(len(R), 1)
        array_compare(R, np.eye(4))
        self.assertIsInstance(R, SE3)

        # random
        R = SE3.Rand()
        nt.assert_equal(len(R), 1)
        self.assertIsInstance(R, SE3)

        # copy constructor
        R = SE3.Rx(pi / 2)
        R2 = SE3(R)
        R = SE3.Ry(pi / 2)
        array_compare(R2, trotx(pi / 2))

    def test_listpowers(self):
        R = SE3()
        R1 = SE3.Rx(0.2)
        R2 = SE3.Ry(0.3)

        R.append(R1)
        R.append(R2)
        nt.assert_equal(len(R), 3)
        self.assertIsInstance(R, SE3)

        array_compare(R[0], np.eye(4))
        array_compare(R[1], R1)
        array_compare(R[2], R2)

        R = SE3([trotx(0.1), trotx(0.2), trotx(0.3)])
        nt.assert_equal(len(R), 3)
        self.assertIsInstance(R, SE3)
        array_compare(R[0], trotx(0.1))
        array_compare(R[1], trotx(0.2))
        array_compare(R[2], trotx(0.3))

        R = SE3([SE3.Rx(0.1), SE3.Rx(0.2), SE3.Rx(0.3)])
        nt.assert_equal(len(R), 3)
        self.assertIsInstance(R, SE3)
        array_compare(R[0], trotx(0.1))
        array_compare(R[1], trotx(0.2))
        array_compare(R[2], trotx(0.3))

    def test_tests(self):

        R = SE3()

        self.assertEqual(R.isrot(), False)
        self.assertEqual(R.isrot2(), False)
        self.assertEqual(R.ishom(), True)
        self.assertEqual(R.ishom2(), False)

    def test_properties(self):

        R = SE3()

        self.assertEqual(R.isSO, False)
        self.assertEqual(R.isSE, True)

        array_compare(R.n, np.r_[1, 0, 0])
        array_compare(R.n, np.r_[1, 0, 0])
        array_compare(R.n, np.r_[1, 0, 0])

        nt.assert_equal(R.N, 3)
        nt.assert_equal(R.shape, (4, 4))

    def test_arith(self):
        T = SE3(1, 2, 3)

        # sum
        a = T + T
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[2, 0, 0, 2], [0, 2, 0, 4], [0, 0, 2, 6], [0, 0, 0, 2]]))

        a = T + 1
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[2, 1, 1, 2], [1, 2, 1, 3], [1, 1, 2, 4], [1, 1, 1, 2]]))

        # a = 1 + T
        # self.assertNotIsInstance(a, SE3)
        # array_compare(a, np.array([ [2,1,1], [1,2,1], [1,1,2]]))

        a = T + np.eye(4)
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[2, 0, 0, 1], [0, 2, 0, 2], [0, 0, 2, 3], [0, 0, 0, 2]]))

        # a =  np.eye(3) + T
        # self.assertNotIsInstance(a, SE3)
        # array_compare(a, np.array([ [2,0,0], [0,2,0], [0,0,2]]))
        #  this invokes the __add__ method for numpy

        a = T
        a += T
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[2, 0, 0, 2], [0, 2, 0, 4], [0, 0, 2, 6], [0, 0, 0, 2]]))

        a = T
        a += 1
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[2, 1, 1, 2], [1, 2, 1, 3], [1, 1, 2, 4], [1, 1, 1, 2]]))

        # difference
        T = SE3(1, 2, 3)

        a = T - T
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.zeros((4, 4)))

        a = T - 1
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[0, -1, -1, 0], [-1, 0, -1, 1], [-1, -1, 0, 2], [-1, -1, -1, 0]]))

        # a = 1 - T
        # self.assertNotIsInstance(a, SE3)
        # array_compare(a, -np.array([ [0,-1,-1], [-1,0,-1], [-1,-1,0]]))

        a = T - np.eye(4)
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[0, 0, 0, 1], [0, 0, 0, 2], [0, 0, 0, 3], [0, 0, 0, 0]]))

        # a =  np.eye(3) - T
        # self.assertNotIsInstance(a, SE3)
        # array_compare(a, np.zeros((3,3)))

        a = T
        a -= T
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.zeros((4, 4)))

        a = T
        a -= 1
        self.assertNotIsInstance(a, SE3)
        array_compare(a, np.array([[0, -1, -1, 0], [-1, 0, -1, 1], [-1, -1, 0, 2], [-1, -1, -1, 0]]))

        # multiply
        T = SE3(1, 2, 3)

        a = T * T
        self.assertIsInstance(a, SE3)
        array_compare(a, transl(2, 4, 6))

        a = T * 2
        self.assertNotIsInstance(a, SE3)
        array_compare(a, 2 * transl(1, 2, 3))

        a = 2 * T
        self.assertNotIsInstance(a, SE3)
        array_compare(a, 2 * transl(1, 2, 3))

        T = SE3(1, 2, 3)
        T *= SE3.Ry(pi / 2)
        self.assertIsInstance(T, SE3)
        array_compare(T, np.array([[0, 0, 1, 1], [0, 1, 0, 2], [-1, 0, 0, 3], [0, 0, 0, 1]]))

        T = SE3()
        T *= 2
        self.assertNotIsInstance(T, SE3)
        array_compare(T, 2 * np.eye(4))

        array_compare(SE3.Rx(pi / 2) * SE3.Ry(pi / 2) * SE3.Rx(-pi / 2), SE3.Rz(pi / 2))

        array_compare(SE3.Ry(pi / 2) * [1, 0, 0], np.r_[0, 0, -1])

        # SE3 x vector
        vx = np.r_[1, 0, 0]
        vy = np.r_[0, 1, 0]
        vz = np.r_[0, 0, 1]

        def cv(v):
            return np.c_[v]

        nt.assert_equal(isinstance(SE3.Tx(pi / 2) * vx, np.ndarray), True)
        array_compare(SE3.Rx(pi / 2) * vx, vx)
        array_compare(SE3.Rx(pi / 2) * vy, vz)
        array_compare(SE3.Rx(pi / 2) * vz, -vy)

        array_compare(SE3.Ry(pi / 2) * vx, -vz)
        array_compare(SE3.Ry(pi / 2) * vy, vy)
        array_compare(SE3.Ry(pi / 2) * vz, vx)

        array_compare(SE3.Rz(pi / 2) * vx, vy)
        array_compare(SE3.Rz(pi / 2) * vy, -vx)
        array_compare(SE3.Rz(pi / 2) * vz, vz)

        # divide
        T = SE3.Ry(0.3)
        a = T / T
        self.assertIsInstance(a, SE3)
        array_compare(a, np.eye(4))

        a = T / 2
        self.assertNotIsInstance(a, SE3)
        array_compare(a, troty(0.3) / 2)

    def test_arith_vect(self):

        rx = SE3.Rx(pi / 2)
        ry = SE3.Ry(pi / 2)
        rz = SE3.Rz(pi / 2)
        u = SE3()

        # multiply
        T = SE3([rx, ry, rz])
        a = T * rx
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * rx)
        array_compare(a[2], rz * rx)

        a = rx * T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], rx * ry)
        array_compare(a[2], rx * rz)

        a = T * T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * ry)
        array_compare(a[2], rz * rz)

        a = T * 2
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * 2)
        array_compare(a[1], ry * 2)
        array_compare(a[2], rz * 2)

        a = 2 * T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * 2)
        array_compare(a[1], ry * 2)
        array_compare(a[2], rz * 2)

        a = T
        a *= rx
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * rx)
        array_compare(a[2], rz * rx)

        a = rx
        a *= T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], rx * ry)
        array_compare(a[2], rx * rz)

        a = T
        a *= T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * rx)
        array_compare(a[1], ry * ry)
        array_compare(a[2], rz * rz)

        a = T
        a *= 2
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx * 2)
        array_compare(a[1], ry * 2)
        array_compare(a[2], rz * 2)

        # SE3 x vector
        vx = np.r_[1, 0, 0]
        vy = np.r_[0, 1, 0]
        vz = np.r_[0, 0, 1]

        a = T * vx
        array_compare(a[:, 0], (rx * vx).flatten())
        array_compare(a[:, 1], (ry * vx).flatten())
        array_compare(a[:, 2], (rz * vx).flatten())

        a = rx * np.vstack((vx, vy, vz)).T
        array_compare(a[:, 0], (rx * vx).flatten())
        array_compare(a[:, 1], (rx * vy).flatten())
        array_compare(a[:, 2], (rx * vz).flatten())

        # divide
        T = SE3([rx, ry, rz])
        a = T / rx
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], ry / rx)
        array_compare(a[2], rz / rx)

        a = rx / T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], rx / ry)
        array_compare(a[2], rx / rz)

        a = T / T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], np.eye(4))
        array_compare(a[1], np.eye(4))
        array_compare(a[2], np.eye(4))

        a = T / 2
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / 2)
        array_compare(a[1], ry / 2)
        array_compare(a[2], rz / 2)

        a = T
        a /= rx
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], ry / rx)
        array_compare(a[2], rz / rx)

        a = rx
        a /= T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / rx)
        array_compare(a[1], rx / ry)
        array_compare(a[2], rx / rz)

        a = T
        a /= T
        self.assertIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], np.eye(4))
        array_compare(a[1], np.eye(4))
        array_compare(a[2], np.eye(4))

        a = T
        a /= 2
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx / 2)
        array_compare(a[1], ry / 2)
        array_compare(a[2], rz / 2)

        # add
        T = SE3([rx, ry, rz])
        a = T + rx
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + rx)
        array_compare(a[2], rz + rx)

        a = rx + T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], rx + ry)
        array_compare(a[2], rx + rz)

        a = T + T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + ry)
        array_compare(a[2], rz + rz)

        a = T + 1
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + 1)
        array_compare(a[1], ry + 1)
        array_compare(a[2], rz + 1)

        a = T
        a += rx
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + rx)
        array_compare(a[2], rz + rx)

        a = rx
        a += T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], rx + ry)
        array_compare(a[2], rx + rz)

        a = T
        a += T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + rx)
        array_compare(a[1], ry + ry)
        array_compare(a[2], rz + rz)

        a = T
        a += 1
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx + 1)
        array_compare(a[1], ry + 1)
        array_compare(a[2], rz + 1)

        # subtract
        T = SE3([rx, ry, rz])
        a = T - rx
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - rx)
        array_compare(a[2], rz - rx)

        a = rx - T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], rx - ry)
        array_compare(a[2], rx - rz)

        a = T - T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - ry)
        array_compare(a[2], rz - rz)

        a = T - 1
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - 1)
        array_compare(a[1], ry - 1)
        array_compare(a[2], rz - 1)

        a = T
        a -= rx
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - rx)
        array_compare(a[2], rz - rx)

        a = rx
        a -= T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], rx - ry)
        array_compare(a[2], rx - rz)

        a = T
        a -= T
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - rx)
        array_compare(a[1], ry - ry)
        array_compare(a[2], rz - rz)

        a = T
        a -= 1
        self.assertNotIsInstance(a, SE3)
        nt.assert_equal(len(a), 3)
        array_compare(a[0], rx - 1)
        array_compare(a[1], ry - 1)
        array_compare(a[2], rz - 1)

    def test_functions(self):
        # inv
        # .T
        pass

    def test_functions_vect(self):
        # inv
        # .T
        pass

class Twist3dTest(unittest.TestCase):
    
    def test_constructor(self):
        
        s = [1, 2, 3, 4, 5, 6]
        x = Twist(s)
        self.assertIsInstance(x, Twist)
        self.assertEqual(len(x), 1)
        array_compare(x.v, [1, 2, 3])
        array_compare(x.w, [4, 5, 6])
        array_compare(x.S, s)
        
        x = Twist([1,2,3], [4,5,6])
        array_compare(x.v, [1, 2, 3])
        array_compare(x.w, [4, 5, 6])
        array_compare(x.S, s)

        y = Twist(x)
        array_compare(x, y)
        
        x = Twist(SE3())
        array_compare(x, [0,0,0,0,0,0])
        
        
    def test_list(self):
        x = Twist([1, 0, 0, 0, 0, 0])
        y = Twist([1, 0, 0, 0, 0, 0])
                   
        a = Twist(x)
        a.append(y)
        self.assertEqual(len(a), 2)
        array_compare(a[0], x)
        array_compare(a[1], y)
        
    def test_conversion_SE3(self):
        T = SE3.Rx(0)
        tw = Twist(T)
        array_compare(tw.SE3, T)
        self.assertIsInstance(tw.SE3, SE3)
        self.assertEqual(len(tw.SE3), 1)

        T = SE3.Rx(0) * SE3(1, 2, 3)
        array_compare(Twist(T).SE3, T)
        
    def test_conversion_se3(self):
        s = [1, 2, 3, 4, 5, 6]
        x = Twist(s)
        
        array_compare(x.se3, np.array([[ 0., -6.,  5.,  1.],
                    [ 6.,  0., -4.,  2.],
                    [-5.,  4.,  0.,  3.],
                    [ 0.,  0.,  0.,  0.]]))
        
    def test_conversion_Plucker(self):
        pass
        
    def test_list_constuctor(self):
        x = Twist([1, 0, 0, 0, 0, 0])
        
        a = Twist([x,x,x,x])
        self.assertIsInstance(a, Twist)
        self.assertEqual(len(a), 4)
        
        a = Twist([x.se3, x.se3, x.se3, x.se3])
        self.assertIsInstance(a, Twist)
        self.assertEqual(len(a), 4)
        
        a = Twist([x.S, x.S, x.S, x.S])
        self.assertIsInstance(a, Twist)
        self.assertEqual(len(a), 4)
        
        s = [1, 2, 3, 4, 5, 6]
        a = Twist([s, s, s, s])
        self.assertIsInstance(a, Twist)
        self.assertEqual(len(a), 4)
        
    def test_predicate(self):
        x = Twist.R([1, 2, 3], [0, 0, 0])
        self.assertFalse(x.isprismatic)
        
        # check prismatic twist
        x = Twist.P([1, 2, 3])
        self.assertTrue(x.isprismatic)
        
        self.assertTrue(Twist.isvalid(x.se3))
        self.assertTrue(Twist.isvalid(x.S))
        
        self.assertFalse(Twist.isvalid(2))
        self.assertFalse(Twist.isvalid(np.eye(4)))
        
    def test_str(self):
        x = Twist([1, 2, 3, 4, 5, 6])
        s = str(x)
        self.assertIsInstance(s, str)
        self.assertEqual(len(s), 14)
        self.assertEqual(s.count('\n'), 0)
        
        x.append(x)
        s = str(x)
        self.assertIsInstance(s, str)
        self.assertEqual(len(s), 29)
        self.assertEqual(s.count('\n'), 1)
        
    def test_variant_constructors(self):
        
        # check rotational twist
        x = Twist.R([1, 2, 3], [0, 0, 0])
        array_compare(x, np.r_[0, 0, 0, unitvec([1, 2, 3])])
        
        # check prismatic twist
        x = Twist.P([1, 2, 3])
        array_compare(x, np.r_[unitvec([1, 2, 3]), 0, 0, 0, ])
    
    def test_SE3_twists(self):
        tw = Twist( SE3.Rx(0) )
        array_compare(tw, np.r_[0, 0, 0,  0, 0, 0])
                      
        tw = Twist( SE3.Rx(pi / 2) )
        array_compare(tw, np.r_[0, 0, 0,  pi / 2, 0, 0])
                      
        tw = Twist( SE3.Ry(pi / 2) )
        array_compare(tw, np.r_[0, 0, 0,  0, pi / 2, 0])
                      
        tw = Twist( SE3.Rz(pi / 2) )
        array_compare(tw, np.r_[0, 0, 0,  0, 0, pi / 2])
        
        tw = Twist( SE3([1, 2, 3]) )
        array_compare(tw, [1, 2, 3,  0, 0, 0])
                      
        tw = Twist( SE3([1, 2, 3]) * SE3.Ry(pi / 2))
        array_compare(tw, np.r_[-pi / 2, 2, pi,  0, pi / 2, 0])
        
    def test_exp(self):
        tw = Twist.R([1, 0, 0], [0, 0, 0])
        array_compare(tw.exp(pi/2), SE3.Rx(pi/2))
        
        tw = Twist.R([0, 1, 0], [0, 0, 0])
        array_compare(tw.exp(pi/2), SE3.Ry(pi/2))
        
        tw = Twist.R([0, 0, 1], [0, 0, 0])
        array_compare(tw.exp(pi/2), SE3.Rz(pi / 2))
    
    def test_arith(self):
        
        # check overloaded *

        T1 = SE3(1, 2, 3) * SE3.Rx(pi / 2)
        T2 = SE3(4, 5, -6) * SE3.Ry(-pi / 2)
        
        x1 = Twist(T1)
        x2 = Twist(T2)

        array_compare( (x1 * x2).exp(), T1 * T2)
        array_compare( (x2 * x1).exp(), T2 * T1)
        
    def test_prod(self):
        # check prod
        T1 = SE3(1, 2, 3) * SE3.Rx(pi / 2)
        T2 = SE3(4, 5, -6) * SE3.Ry(-pi / 2)
        
        x1 = Twist(T1)
        x2 = Twist(T2)
        
        x = Twist([x1, x2])
        array_compare( x.prod().SE3, T1 * T2)
        



# ---------------------------------------------------------------------------------------#
if __name__ == '__main__':

    unittest.main()
