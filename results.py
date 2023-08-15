import os
import csv
import sys
import numpy as np
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats


def expect_max(list_values):
    max_values = []
    for i in range(1000):
        max_values.append(np.amax(np.random.choice(list_values, 50)))

    return np.mean(max_values), np.std(max_values)


def probability(list_values, threshold):
    counter = 0
    for i in range(1000):
        if np.amax(np.random.choice(list_values, 50)) > threshold:
            counter += 1
    return counter / 1000


dir = os.listdir("Results")
model = sys.argv[1]

for file in dir:
    if file.endswith(".csv") and model in file:
        with open("Results/" + file, 'r') as f:
            reader = csv.reader(f)

            next(reader)

            max_values = []

            for row in reader:

                values = row[-2:]
                values = np.array(values, dtype=float)
                
                # Get the maximum value of the row
                max_val = np.amax(values)
                max_values.append(max_val)

expect_max_mean, expect_max_std = expect_max(max_values)
probability = probability(max_values, 0.5)

print("Expected maximum value: ", expect_max_mean)
print("Standard deviation of expected maximum value: ", expect_max_std)
print("Probability of maximum value > 0.5: ", probability)