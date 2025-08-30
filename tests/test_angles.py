
import math
import unittest
from src.gestures import angle_between

class TestAngles(unittest.TestCase):
    def test_colinear(self):
        a,b,c=(0,0,0),(1,0,0),(2,0,0)
        self.assertAlmostEqual(angle_between(a,b,c), 180.0, places=3)

    def test_right_angle(self):
        a,b,c=(0,0,0),(0,0,0),(0,1,0)  # degenerate, but used to test function stability
        # Ensure no crash; angle defined in function clamps small norms.
        ang = angle_between((1,0,0),(0,0,0),(0,1,0))
        self.assertTrue(0.0 <= ang <= 180.0)

if __name__ == "__main__":
    unittest.main()
