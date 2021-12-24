# Library contaning functions that edit the sound data


import math
from functions import *


def freqcalc(l):
    """ Calculates the frequence of a list of samples
        frequency is defined as the distance (number of samples) between
        a zero and another """

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


def freqcalc2(l):
    """ Calculates the frequence of a list of samples
        frequency is defined as the distance between two hights with between
        them at least a negative value """

    freq_list = []

    sign = 1
    oldbestidx = 0
    best, bestidx = 0, 0

    for i in range(len(l)):

        if getsign(l[i]) != sign:
            if sign == 1:

                # append the last frequency
                freq_list.extend([bestidx-oldbestidx+1]
                                 * (bestidx-oldbestidx+1))

                oldbestidx = bestidx
                best, bestidx = 0, 0
            sign = getsign(l[i])

        if l[i] > best:
            best = l[i]
            bestidx = i

    freq_list.extend([bestidx-oldbestidx] * (bestidx-oldbestidx))
    return freq_list


data = wavreader("tredowav.wav")

ch1 = data["data"]["ch1"][:]
ch2 = data["data"]["ch2"]
freqs = freqcalc(ch1)

fig, ax = plt.subplots()

ax2 = ax.twinx()


ax.grid()
ax.plot(ch1)
ax2.plot(freqs, color="red", linewidth=0.3)

ax.set_ylabel("int")
ax2.set_ylabel("Hertz")
ax.axhline(0, color="black", alpha=0.5)
ax2.axhline(0, color="black", alpha=0.5)


plt.savefig("plot.png", dpi=600)
