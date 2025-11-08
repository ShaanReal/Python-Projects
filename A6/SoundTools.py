# SoundTools.py
# Functions to process audio samples.
# For CS 1400, written by David E. Johnson.
# Function implementations by Shaan Luthra

import random

# --------------------------------------------------------------------
# make_reversed_samples
# Returns a new list with the elements of the input list reversed.
def make_reversed_samples(samples):
    new_samples = []
    for val in samples:
        new_samples.insert(0, val)  # add each new value at the start
    return new_samples


# --------------------------------------------------------------------
# make_louder_samples
# Returns a new list where each sample is multiplied by the given scale factor.
def make_louder_samples(samples, scale):
    new_samples = []
    for val in samples:
        new_samples.append(val * scale)
    return new_samples


# --------------------------------------------------------------------
# make_clipped_samples
# Returns a new list where all values are limited to the range [-clip_level, clip_level].
def make_clipped_samples(samples, clip_level):
    new_samples = []
    for val in samples:
        if val > clip_level:
            new_samples.append(clip_level)
        elif val < -clip_level:
            new_samples.append(-clip_level)
        else:
            new_samples.append(val)
    return new_samples


# --------------------------------------------------------------------
# make_noisy_samples
# Returns a new list where random noise from -noise_level to +noise_level
# is added to each sample.
def make_noisy_samples(samples, noise_level):
    new_samples = []
    for val in samples:
        noise = random.randint(-noise_level, noise_level)
        new_samples.append(val + noise)
    return new_samples


# --------------------------------------------------------------------
# make_smoothed_samples
# Returns a new list where each sample is the average of its neighbors.
# Uses integer truncation (int()).
def make_smoothed_samples(samples):
    if len(samples) < 2:
        return samples[:]  # not enough to smooth
    new_samples = []

    # first value: average of first two
    new_samples.append(int((samples[0] + samples[1]) / 2))

    # middle values: average of previous, current, next
    for i in range(1, len(samples) - 1):
        avg = int((samples[i - 1] + samples[i] + samples[i + 1]) / 3)
        new_samples.append(avg)

    # last value: average of last two
    new_samples.append(int((samples[-2] + samples[-1]) / 2))
    return new_samples


# --------------------------------------------------------------------
# make_echo_samples
# Returns a new list where an echo effect is added after a delay (offset)
# and scaled by echo_weight.
def make_echo_samples(samples, offset, echo_weight):
    new_samples = []
    length = len(samples)

    # Part 1: copy the first offset samples
    for i in range(offset):
        new_samples.append(samples[i])

    # Part 2: add echo to the rest
    for i in range(offset, length):
        echo_val = int(samples[i] + samples[i - offset] * echo_weight)
        new_samples.append(echo_val)

    # Part 3: add the trailing echo values
    for i in range(length - offset, length):
        tail_val = int(samples[i] * echo_weight)
        new_samples.append(tail_val)

    return new_samples


# --------------------------------------------------------------------
# main
# Simple tests for each function using small, predictable lists.
def main():
    print("Testing make_reversed_samples")
    data = [1, 2, 3]
    print("Input:", data)
    print("Expected: [3, 2, 1]")
    print("Actual:", make_reversed_samples(data))
    print()

    print("Testing make_louder_samples")
    data = [1, 2, 3]
    print("Input:", data)
    print("Scale: 2")
    print("Expected: [2, 4, 6]")
    print("Actual:", make_louder_samples(data, 2))
    print()

    print("Testing make_clipped_samples")
    data = [-5, -1, 2, 5, 10]
    print("Input:", data)
    print("Clip level: 4")
    print("Expected: [-4, -1, 2, 4, 4]")
    print("Actual:", make_clipped_samples(data, 4))
    print()

    print("Testing make_noisy_samples")
    data = [10, 20, 30]
    print("Input:", data)
    print("Noise level: 2")
    print("Expected: Each value slightly different (random noise added)")
    print("Actual:", make_noisy_samples(data, 2))
    print()

    print("Testing make_smoothed_samples")
    data = [0, 100, 500, -100]
    print("Input:", data)
    print("Expected: [50, 200, 166, 200]")
    print("Actual:", make_smoothed_samples(data))
    print()

    print("Testing make_echo_samples")
    data = [10, 20, 30, 40]
    print("Input:", data)
    print("Offset: 1, Weight: 0.5")
    print("Expected: [10, 25, 40, 55, 20]")
    print("Actual:", make_echo_samples(data, 1, 0.5))
    print()

    print("Offset: 2, Weight: 0.5")
    print("Expected: [10, 20, 35, 50, 15, 20]")
    print("Actual:", make_echo_samples(data, 2, 0.5))
    print()


if __name__ == "__main__":
    main()
