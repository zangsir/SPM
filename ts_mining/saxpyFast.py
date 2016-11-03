#!/usr/bin/env python

import os
import numpy as np
import math


class SAX(object):
    """
    This class is for computing common things with the Symbolic
    Aggregate approXimation method.  In short, this translates
    a series of data to a string, which can then be compared with other
    such strings using a lookup table.
    """
    #windowSize is the size of an analysis window for converting to SAX. This is useful in the sliding window case when you slide the window across a very long time-series. If the input is pre-extracted subsequence (e.g., size 30 per ts), then put windwoSize as 30 (the same as the length of subsequence) so there is effectively no sliding window. 
    def __init__(self, windowSize = 30, wordSize = 8, alphabetSize = 7, epsilon = 1e-6):

        if alphabetSize < 3 or alphabetSize > 20:
            raise DictionarySizeIsNotSupported()
        self.wordSize = wordSize
        self.windowSize = windowSize
        self.alphabetSize = alphabetSize
        self.eps = epsilon
        self.breakpoints = {2 : [0],
                            3 : [-0.43, 0.43],
                            4 : [-0.67, 0, 0.67],
                            5 : [-0.84, -0.25, 0.25, 0.84],
                            6 : [-0.97, -0.43, 0, 0.43, 0.97],
                            7 : [-1.07, -0.57, -0.18, 0.18, 0.57, 1.07],
                            8 : [-1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15],
                            9 : [-1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22],
                            10: [-1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28],
                            11: [-1.34, -0.91, -0.6, -0.35, -0.11, 0.11, 0.35, 0.6, 0.91, 1.34],
                            12: [-1.38, -0.97, -0.67, -0.43, -0.21, 0, 0.21, 0.43, 0.67, 0.97, 1.38],
                            13: [-1.43, -1.02, -0.74, -0.5, -0.29, -0.1, 0.1, 0.29, 0.5, 0.74, 1.02, 1.43],
                            14: [-1.47, -1.07, -0.79, -0.57, -0.37, -0.18, 0, 0.18, 0.37, 0.57, 0.79, 1.07, 1.47],
                            15: [-1.5, -1.11, -0.84, -0.62, -0.43, -0.25, -0.08, 0.08, 0.25, 0.43, 0.62, 0.84, 1.11, 1.5],
                            16: [-1.53, -1.15, -0.89, -0.67, -0.49, -0.32, -0.16, 0, 0.16, 0.32, 0.49, 0.67, 0.89, 1.15, 1.53],
                            17: [-1.56, -1.19, -0.93, -0.72, -0.54, -0.38, -0.22, -0.07, 0.07, 0.22, 0.38, 0.54, 0.72, 0.93, 1.19, 1.56],
                            18: [-1.59, -1.22, -0.97, -0.76, -0.59, -0.43, -0.28, -0.14, 0, 0.14, 0.28, 0.43, 0.59, 0.76, 0.97, 1.22, 1.59],
                            19: [-1.62, -1.25, -1, -0.8, -0.63, -0.48, -0.34, -0.2, -0.07, 0.07, 0.2, 0.34, 0.48, 0.63, 0.8, 1, 1.25, 1.62],
                            20: [-1.64, -1.28, -1.04, -0.84, -0.67, -0.52, -0.39, -0.25, -0.13, 0, 0.13, 0.25, 0.39, 0.52, 0.67, 0.84, 1.04, 1.28, 1.64]
                            }
        self.beta = self.breakpoints[self.alphabetSize]
        self.build_dist_table()


    def to_letter_rep(self, x):
        """
        Function takes a series of data, x, and transforms it to a string representation
        """
        if self.windowSize > len(x):
            print "ERROR: input length too short comparing to the windowSize of ", self.windowSize
            return
        all_saxString = []
        pointers = []
        for i in range(len(x) - (self.windowSize-1)):
            sub_section = x[i:i + self.windowSize]
            #print i
            paaX = self.to_PAA(self.normalize(sub_section))
            #print "PAA:",paaX
            saxString = self.alphabetize(paaX)
            all_saxString.append(saxString)
            pointers.append(i)
        return all_saxString, pointers


    def normalize(self, x):
        """
        Function will normalize an array (give it a mean of 0, and a
        standard deviation of 1) unless it's standard deviation is below
        epsilon, in which case it returns an array of zeros the length
        of the original array.
        """
        X = np.asanyarray(x)
        if X.std() < self.eps:
            return [0 for entry in X]
        return (X-X.mean())/X.std()

    def to_PAA(self, x):
        """
        Funciton performs Piecewise Aggregate Approximation on data set, reducing
        the dimension of the dataset x to w discrete levels. returns the reduced
        dimension data set, as well as the indicies corresponding to the original
        data for each reduced dimension
        """
        windowSize = self.windowSize
        wordSize = self.wordSize
        if windowSize == wordSize:
            PAA = x
        else:
            if windowSize%wordSize!=0:
                #print 'case1'
                temp = np.zeros((wordSize,windowSize))
                for j in xrange(wordSize):
                    temp[j,:] = x
                expanded_sub_section = np.ndarray.flatten(temp,'F')
                PAA = np.mean(np.reshape(expanded_sub_section, (wordSize, windowSize)).transpose(),axis=0)
            else:
                #print 'case2'
                win_size = windowSize/wordSize
                expanded_sub_section = np.ndarray.flatten(x, 'F')
                PAA = np.mean(np.reshape(expanded_sub_section,(wordSize, win_size)).transpose(), axis = 0)
        return PAA
     

    def alphabetize(self,paaX):
        """
        Converts the Piecewise Aggregate Approximation of x to a series of letters.
        """
        alphabetizedX = np.zeros(len(paaX))
        for i in range(len(paaX)):
            alphabetizedX[i] = np.sum(self.beta<=paaX[i])+1
            
        return alphabetizedX

    def min_dist(self, sA, sB):
        """
        Compares two strings based on individual letter distance
        Requires that both strings are the same length
        """
        sA = sA.astype(int)
        sB = sB.astype(int)

        if len(sA)!=len(sB):
            print "error: strings must of the same length"
            return
        dist_matrix = self.build_dist_table()
        compression_ratio = float(self.windowSize) / self.wordSize
        #print 'real sA:',sA
        mindist = np.sqrt(compression_ratio * np.sum(dist_matrix[sA-1, sB-1]))

        return mindist

    def compare_letters(self, la, lb):
        """
        Compare two letters based on letter distance return distance between
        """
        return self.compareDict[la+lb]

    def build_dist_table(self):
        """
        Builds up the lookup table to determine numeric distance between two letters
        given an alphabet size.  Entries for both 'ab' and 'ba' will be created
        and will have identical values.
        """
        alphabet_size = self.alphabetSize
        print 'alpha size:',alphabet_size
        dist_matrix = np.zeros((alphabet_size, alphabet_size))
        for i in xrange(alphabet_size):
            # the min_dist for adjacent symbols are 0, so we start with i+2
            for j in xrange(i+2, alphabet_size):
                # square the distance now for future use
                dist_matrix[i, j] = (self.beta[i] - self.beta[j-1])**2
                # the distance matrix is symmetric
                dist_matrix[j,i] = dist_matrix[i, j]
        return dist_matrix

