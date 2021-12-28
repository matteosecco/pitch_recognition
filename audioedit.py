# Library contaning functions that edit the sound data


from matplotlib import pyplot as plt
import math
from functions import smooth, getsign, sinfind, der, mean
from reader import wavreader, wavwriter
from copy import copy


def freqcalc(l):
    """ Calculates the frequence of a list of samples
        frequency is defined as the distance (number of samples) between
        a zero and another
        
        l: list of wave frames
        returns: list containing a value of frequency (actually wavelenght)
        for each value """

    # where to save the frequencies
    freq_list = []
    # current count
    count = 0
    # current sign
    sign = 1.0

    for el in l:

        if math.copysign(1, el) != sign:
            sign = math.copysign(1, el)
            freq_list.extend([count]*count)  # per hertz: 44100/ count+1
            count = 0

        count += 1

    freq_list.extend([count]*count)

    return freq_list


def maxlist(l):
    """ Returns the list of all the local maximum and minimum
        a maximum is defined as the local maximum in an interval where the
        extremesare equal to 0
        
        l: list of wave frames 
        returns: list of tuples (idx, value) """

    sign = getsign(l[0])
    locbest = 0
    idxbest = 0

    # list of 2d tuples
    data = []

    for i in range(len(l)):
        if abs(l[i]) > locbest:
            locbest = abs(l[i])
            idxbest = i

        # the value must be different from 0 to avoid a very rare case where
        # the first derivative is 0 exactly on y=0 so that getsign(0) returns -1
        if getsign(l[i]) != sign and l[i] != 0:
            data.append((idxbest, locbest*sign))
            sign = getsign(l[i])
            locbest = 0

    # adds first and last point to coincide with 0
    if data[0][0] != 0:
        data.insert(0, (0, 0))
    data.append((len(l), 0))

    return data


def createsin(l):
    """ Creates a continous function from the list of points 'l'
    
    l: list of wave frames
    returns: list with all the values indexed """

    new_l = []
    # get the list of maximums and minimums
    plist = maxlist(l)

    # cycles all the points
    for i in range(len(plist)-1):

        # for each two point it calculates the right sine function
        a, b, c, d = sinfind(plist[i], plist[i+1])

        # for each two point generates all the point in between them
        for x in range(plist[i][0], plist[i+1][0]):

            value = a*math.sin(b*x + c) + d

            new_l.append(int(value))

    return new_l


def getnote(l, r=44100):
    """ Gets the mean frequency of the list
    
    l: list of wave frames
    r: sample rate per second
    returns: int representing Hertz """

    d = {"do4": 440,
         "do#4": 466,
         "re4": 493,
         "mi5": 523,
         "mi#5": 554,
         "fa5": 587,
         "fa#5": 622,
         "sol5": 659,
         "la5": 698,
         "la#5": 739,
         "si5": 783,
         "si#5": 830,
         "do5": 880}

    hertz = r / mean(freqcalc(l))

    for v in d.values():
        pass

    return
