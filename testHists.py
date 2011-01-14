#!/usr/bin/env python
# encoding: utf-8
"""
testHists.py

Created by Nicholas Devenish on 2011-01-12.
"""

import unittest
import hists
import numpy

class testHist(unittest.TestCase):
  def testSimpleCreation(self):
    "Simple creation routines of a histogram"
    a = hists.Hist([0, 1, 2])
    # Test that this made sensible values
    self.assertEqual(a.data.size, 2)
    self.assertEqual(a.bins, (0, 1, 2))
  
  def testPreserveDtype(self):
    "Tests that numpy array type is preserved"
    data = numpy.array([1, 2, 3], dtype=int)
    bins = [0, 1, 2, 3]
    a = hists.Hist(bins, data=data)
    self.assertEqual(a.data.dtype, data.dtype)
    
  def testCreationWithData(self):
    "Test that data is allocated, and mismatched size data fails"
    a = hists.Hist([0, 1, 2], data=[1, 5])
    self.assertTrue((a.data == numpy.array([1,5])).all())
    self.assertRaises(hists.BinError, hists.Hist, [0, 1, 2], data=[1, 5, 2])
  
  def testFlows(self):
    "Tests that the under/overflows are created properly"  
    a = hists.Hist([0,1,2,3])
    self.assertEqual(a.underflow, 0.0)
    self.assertEqual(a.overflow, 0.0)
    a = hists.Hist([0,1,2,3], numpy.array([0,1,2]))
    self.assertEqual(a.underflow, 0)
    self.assertEqual(a.overflow, 0)
    
    # Change them, and verify that changing the data resets them
    a.underflow = 42
    a.overflow = 99
    a.data = numpy.array([0.,1.,2.])
    self.assertEqual(a.underflow, 0.0)
    self.assertEqual(a.overflow, 0.0)
  
  def testNullCreation(self):
    "Null creation only works for zero bin entries"
    self.assertRaises(hists.BinError, hists.Hist, [0])
  
  def testChangeBins(self):
    """Tests correct behaviour when changing the number of bins"""
    a = hists.Hist([0, 1, 2])
    a.bins = [0, 1]
    self.assertEquals(a.data.size, 1)
    # Check this was turned into a tuple
    def t():
      a[1] = 4
    self.assertRaises(TypeError, t)
    # Check that bins must be in order
    def t():
      a.bins = [0, 2, 1, 3]
    self.assertRaises(hists.BinError, t)
      
    
  def test_bin_count(self):
    """Test the .bincount property makes sense"""
    bins = [0, 1]
    for x in range(2,10):
      bins.append(bins[-1]+1)
      a = hists.Hist(bins)
      self.assertEquals(a.bincount, x)
      self.assertEquals(a.bincount, a.data.size)
  
  def testInplaceArithmetic(self):
    "Tests the in-place arithmetic"
    bins = [0, 1, 2, 3]
    data = numpy.array([3, 1, 2])
    a = hists.Hist(bins, data)
    b = hists.Hist(bins, data)
    
    a += a
    self.assertTrue((a.data == data*2).all())
    a -= b
    self.assertTrue((a.data == data).all())
    a *= b
    self.assertTrue((a.data == data*data).all())
    a /= b
    self.assertTrue((a.data == data).all())
    a //= hists.Hist(bins,data=[2,2,2])
    self.assertTrue((a.data == hists.Hist(bins,data=[1,0,1]).data).all())
    
  def testArithmetic(self):
    "Tests the regular arithmetic"
    bins = [0, 1, 2, 3]
    data = numpy.array([3, 1, 2])
    a = hists.Hist(bins, data)
    b = hists.Hist(bins, data)
    
    c = a + a
    self.assertTrue((c.data == data*2).all())
    c = c - a
    self.assertTrue((c.data == data).all())
    c = a * a
    self.assertTrue((c.data == data*data).all())
    c = c / a
    self.assertTrue((c.data == data).all())
  
  def testNonClassIntegerArithmetic(self):
    "Tests arithmetic against non-Hist class values"
    bins = [0, 1]
    data = numpy.array([2])
    a = hists.Hist(bins, data)
    
    # Forward tests
    self.assertEqual((a + 5).data, 7)
    self.assertEqual((a - 5).data, -3)
    self.assertEqual((a * 10).data, 20)
    self.assertEqual((a / 2).data, 1)

    # Reverse tests
    self.assertEqual((5+a).data, 7)

  def testMismatchedData(self):
    "Checks that we cannot do operations on histograms with mismatched data"
    
    a = hists.Hist([0, 1, 2], data=numpy.zeros(2))
    b = hists.Hist([0, 1, 2], data=numpy.zeros((2,2)))
    
    self.assertRaises(TypeError, a.__add__, b)
    self.assertRaises(TypeError, a.__sub__, b)
    self.assertRaises(TypeError, a.__mul__, b)
    self.assertRaises(TypeError, a.__div__, b)

class testHistFilling(unittest.TestCase):
  def setUp(self):
    pass
    
  def testBasicFill(self):
    "Tests the elementary filling functions"
    a = hists.Hist(range(101))
    a.fill(0.5)
    self.assertEqual(a.data[0], 1.0)
    # And, with weights
    a.fill(1.0, 0.5)
    self.assertEqual(a.data[1], 0.5)
  
  def testFillEdges(self):
    "Tests the filling edge cases"
    a = hists.Hist(range(101))
    # Test that the overflow edge is good
    a.fill(100)
    self.assertEqual(a.data[99], 0.0)
    a.fill(99.9999999)
    self.assertEqual(a.data[99], 1.0)
    a.fill(0)
    self.assertEqual(a.data[0], 1.0)
    
    
  def testFlows1(self):
    "Tests filling the underflow"
    a = hists.Hist(range(101))
    a.fill(-1)
    self.assertEqual(a.underflow, 1.0)

  def testFlows2(self):
    "Test missing the overflow"
    a = hists.Hist(range(101))
    a.fill(99.9999999)
    self.assertEqual(a.overflow, 0.0)

  def testFlows3(self):
    "Test filling the overflow"
    a = hists.Hist(range(101))
    a.fill(100)
    print a.data
    self.assertEqual(a.overflow, 1.0)
    
if __name__ == '__main__':
  unittest.main()