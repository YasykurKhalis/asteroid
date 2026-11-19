import unittest
import pygame
from player import Player
from circleshape import CircleShape


class TriangleHitboxTest(unittest.TestCase):
    def test_hits_and_misses(self):
        plr = Player(100, 100)  # nose points down (+y), base corners at (100±13.3, 80)
        self.assertTrue(plr.collides_with(CircleShape(100, 100, 1)))  # center inside
        self.assertTrue(plr.collides_with(CircleShape(100, 125, 6)))  # touches the nose
        self.assertFalse(plr.collides_with(CircleShape(100, 125, 4)))
        # a circular hitbox would hit this corner area, the triangle does not
        self.assertFalse(plr.collides_with(CircleShape(115, 117, 5)))


if __name__ == "__main__":
    unittest.main()
