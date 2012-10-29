# testing qrgen
import unittest
import qrgen

class TestUtilityFunctions(unittest.TestCase):

        def test_random_identifier(self):
                # this is hard to test because of random it could just fail at
                # any time, because of dumb 'luck'
                li = []
                for i in range(0,100):
                        li.append(qrgen.random_identifier())
                print li
                print 'list should have been printed'
                self.assertTrue(len(li)==len(set(li)))

if __name__ == '__main__':
        unittest.main()
