#!/usr/bin/env python

# This is assuming standard tuning for both bass and guitar
# Define guitar string frequencies
GUITAR_HIGH_E_STRING = 329.63
GUITAR_B_STRING = 246.94
GUITAR_G_STRING = 196.00
GUITAR_D_STRING = 146.83
GUITAR_A_STRING = 110.00
GUITAR_LOW_E_STRING = 82.41

GUITAR_STRINGS = {GUITAR_HIGH_E_STRING, GUITAR_A_STRING, GUITAR_D_STRING, GUITAR_G_STRING, GUITAR_B_STRING,
                  GUITAR_LOW_E_STRING}

# Define bass string frequencies
BASS_C_STRING = 130.813
BASS_G_STRING = 97.999
BASS_D_STRING = 97.416
BASS_A_STRING = 55.000
BASS_E_STRING = 41.204
BASS_B_STRING = 30.868

BASS_STRINGS = {BASS_B_STRING, BASS_E_STRING, BASS_A_STRING, BASS_D_STRING, BASS_G_STRING, BASS_C_STRING}


# Frequency can be calculated by dividing velocity by wavelength
def calculate_frequency(velocity, wavelength):
    return velocity / wavelength


# Frequency can also be calculated by 1 divided by period
# The period being the amount of time it takes to complete one wave cycle
def calculate_frequency_period(period):
    return 1 / period


# When a frequency is given find the closest guitar string to compare it too
def find_comparison_string_guitar(freq):
    # Set up variables to return
    comparison_frequency = 0
    min_distance = 10000

    # Go through the guitar strings to find the nearest string
    for string in GUITAR_STRINGS:
        diff = abs(string - freq)
        if diff < min_distance:
            comparison_frequency = string
            min_distance = abs(string - freq)

    return comparison_frequency


# When a frequency is given find the closest bass string to compare it too
def find_comparison_string_bass(freq):
    comparison_frequency = 0
    min_distance = 10000

    # Go through the guitar strings to find the nearest string
    for string in GUITAR_STRINGS:
        diff = abs(string - freq)
        if diff < min_distance:
            comparison_frequency = string
            min_distance = abs(string - freq)

    return comparison_frequency


# Print the name of the known string with the input frequency
def print_string(frequency):
    if frequency == GUITAR_HIGH_E_STRING:
        return "GUITAR_HIGH_E_STRING"
    elif frequency == GUITAR_B_STRING:
        return "GUITAR_B_STRING"
    elif frequency == GUITAR_G_STRING:
        return "GUITAR_G_STRING"
    elif frequency == GUITAR_D_STRING:
        return "GUITAR_D_STRING"
    elif frequency == GUITAR_A_STRING:
        return "GUITAR_A_STRING"
    elif frequency == GUITAR_LOW_E_STRING:
        return "GUITAR_LOW_E_STRING"
    elif frequency == BASS_C_STRING:
        return "BASS_C_STRING"
    elif frequency == BASS_G_STRING:
        return "BASS_G_STRING"
    elif frequency == BASS_D_STRING:
        return "BASS_D_STRING"
    elif frequency == BASS_A_STRING:
        return "BASS_A_STRING"
    elif frequency == BASS_E_STRING:
        return "BASS_E_STRING"
    elif frequency == BASS_B_STRING:
        return "BASS_B_STRING"
    else:
        return "unknown"


# Compare the string with the calculated comparison string
def compare(actual, compared):
    if actual > compared:
        return "sharp"
    elif actual < compared:
        return "flat"
    else:
        return "tuned"


# The main function to tune a string
def tune(freq):
    comparison = find_comparison_string_guitar(freq)
    result = compare(freq, comparison)
    print(print_string(comparison) + ": " + result)


def main():
    print("find_comparison_string_guitar(102.25)")
    comparison = find_comparison_string_guitar(102.25)
    print("Result: " + print_string(comparison))
    print("compare(comparison, GUITAR_A_STRING)")
    print("Result: " + compare(102.25, GUITAR_A_STRING))

    print("\ntune(158.387)")
    tune(158.387)


main()
