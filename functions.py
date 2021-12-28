# Library containing various math functions


from math import asin


def mean(l):
    """ Mean of a list """
    return sum(l) / len(l)


def getsign(i):
    """ Sign of an integer """
    return 1 if i > 0 else -1


def smooth(l, n=15, i=False):
    """ Takes a list and returns it smoothed
        In the range (1, n) each mean must be done with that number of elements
        
        n: 2n+1 is the range of the moving average
        i: whether or not data should be casted to int
        returns: a list
    """

    # creates new list and appends the first element
    new_l = [l[0]]

    for i in range(1, len(l)-1):

        # corrected_n is the range around the 'i'th element
        # it is not always equal to 'n' because in the first and last 'n' elements
        # it is equal to the largest possible range
        if i < n:
            corrected_n = i
        elif len(l) - i < n:
            corrected_n = len(l) - i
        else:
            corrected_n = n

        # temp list with the elements used to calculate the mean
        temp_l = l[i-corrected_n:i+corrected_n+1]

        # if requested, cast all values to int
        if i:
            new_l.append(int(mean(temp_l)))
        else:
            new_l.append(mean(temp_l))

    # appends last element
    new_l.append(l[-1])

    return new_l


def norm(l, n=1):
    """ Normalize a list so that it starts from 'n' """

    # moltiplicatore
    molt = n / l[0]

    return [e*molt for e in l]


def der(l):
    """ Returns the list of the derivative computed on each value of 'l'
    
    l: function values
    returns: new list of the derivatives """

    new_l = []
    for i in range(len(l)-1):

        # correctets ZeroDivisionError
        if l[i] == 0:
            a = 1
        else:
            a = l[i]

        new_l.append((l[i+1] - a) / a)

    return new_l


def sinfind(pa, pb):
    """ Finds a sine wave that passes thorugh
    
    a: tuple containing (x, y) position of point A
    b: tuple containing (x, y) position of point B
    returns: (a, b, c, d) where a*sin(b*X + c) + d = Y """
    # the system to solve is:
    # {a*sin(b*pa[0] + c) + d = pa[1]
    # {a*sin(b*pb[0] + c) + d = pb[1]
    # and 'a' and 'd' are found geometrically

    # xa < xb sempre?? è richiesto? SI ??
    a = (pb[1] - pa[1]) / 2
    d = (pb[1] + pa[1]) / 2

    try:
        # found solving the system
        b = (asin((pb[1]-d) / a) - asin((pa[1]-d) / a)) / (pb[0] - pa[0])
        c = asin((pa[1]-d) / a) - b*pa[0]
    except ZeroDivisionError:
        print(pa, pb)

    return a, b, c, d
