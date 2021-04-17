#!/usr/bin/python3

import csv
import matplotlib.pyplot as plt
import numpy as np

irow = 0

X = []
Y = []

with open('calibration.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    for row in reader:

        if irow == 0:

            ylab = row[0]
            xlab = row[1]

        else :

            Y.append(float(row[0]))
            X.append(float(row[1]))

        irow += 1

fit = np.polyfit(X, Y, 1)

Yfit = fit[0]*np.array(X) + fit[1]

Yres = np.array(Y) - Yfit
print("Standard deviation = "+str(np.std(Yres)))
print("Standard error of the mean = "+str(np.std(Yres)/np.sqrt(len(X))))

plt.plot(X, Y, 'ro')
plt.plot(X, Yfit, 'b-')
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title("V$_{\mathrm{actual}}$ = "+str(fit[0])+" V$_{\mathrm{read}}$ + "+str(fit[1]))

plt.show()

# Theoretical conversion is V_actual = 1.666 * V_read
