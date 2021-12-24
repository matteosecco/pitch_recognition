# Library containing various math functions


def mean(l):
    """ Mean of a list """
    return sum(l) / len(l)


def getsign(i):
    """ Sign of an integer """
    return 1 if i > 0 else -1


def smooth(l, n=15):
    """ Takes a list and returns it smoothed
        In the range (1, n) each mean must be done with that number of elements
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
        new_l.append(mean(temp_l))

    # appends last element
    new_l.append(l[-1])

    return new_l


def norm(l, n=1):
    """ Normalize a list so that it starts from 'n' """

    # moltiplicatore
    molt = n / l[0]

    return [e*molt for e in l]
