"""
File: rmpvisualization.py
---------------------
This code was originally written by Nick Bowman and Katie Creel at Stanford University
and adapted by Noelle Brown for use in CS 1400 at the University of Utah.
The original assignment was created by Colin Kincaid, Annie Hu, Jennie Yang, and Monica Anuforo.

This file visualizes the data using functions you wrote in rmpdataanalysis-solutions.py.

You should not modify any of the contents of this file.
"""

# Necessary imports, including the code you wrote in rmpdataanalysis-solutions.py!
import tkinter
from rmpdataanalysis import *

# Provided constants to load and plot the word frequency data
# Constants are values that remain the same throughout a program's execution.
# You'll notice that these variable names are formatted differently than we are used to seeing - this is intentional!
# In Python, the convention for constants is to use all uppercase letters.
# This formatting signals to other developers that these variables are meant to stay unchanged.
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

FILENAME = "full-data.txt"

VERTICAL_MARGIN = 30
LEFT_MARGIN = 60
RIGHT_MARGIN = 30
LABELS = ["Low Reviews", "Medium Reviews", "High Reviews"]
LABEL_OFFSET = 10
BAR_WIDTH = 75
LINE_WIDTH = 2
TEXT_DX = 2
NUM_VERTICAL_DIVISIONS = 7
TICK_WIDTH = 15


def make_gui(top, width, height, m_word_data, w_word_data, plot_word, search_words):
    """
    Set up the GUI elements for visualizing the Bias Bars, returning the Canvas to use.
    top is TK root, width/height is canvas size, word_data is Bias Bars Data dict.
    """
    # word entry field
    label = tkinter.Label(top, text="Word To Plot:")
    label.grid(row=0, column=0, sticky='w')
    entry = tkinter.Entry(top, width=40, name='entry', borderwidth=2)
    entry.grid(row=0, column=1, sticky='w')
    entry.focus()
    error_out = tkinter.Text(top, height=2, width=70, name='errorout', borderwidth=2)
    error_out.grid(row=0, column=2, sticky='w')

    # canvas for drawing
    canvas = tkinter.Canvas(top, width=width, height=height, name='canvas')
    canvas.grid(row=1, columnspan=12, sticky='w')

    space = tkinter.LabelFrame(top, width=10, height=10, borderwidth=0)
    space.grid(row=2, columnspan=12, sticky='w')

    # Search field etc. at the bottom
    label = tkinter.Label(top, text="Search:")
    label.grid(row=3, column=0, sticky='w')
    search_entry = tkinter.Entry(top, width=40, name='searchentry')
    search_entry.grid(row=3, column=1, sticky='w')
    search_out = tkinter.Text(top, height=2, width=70, name='searchout', borderwidth=2)
    search_out.grid(row=3, column=2, sticky='w')

    # When <return> key is hit in a text field .. connect to the handle_draw()
    # and handle_search() functions to do the work.
    entry.bind("<Return>", lambda event: handle_plot(entry, canvas, m_word_data, w_word_data, error_out, plot_word))
    search_entry.bind("<Return>", lambda event: handle_search(search_entry, search_out, m_word_data, w_word_data, search_words))

    top.update()
    return canvas


def handle_plot(entry, canvas, m_word_data, w_word_data, error_out, plot):
    """
    Called when <return> key is hit in given entry text field.
    Gets search text from given entry, draws results
    to the given canvas.
    """
    text = entry.get().strip().lower()

    error_out.delete('1.0', tkinter.END)
    if not text:
        error_out.insert('1.0', "Please enter a non-empty word.")
    elif " " in text:
        error_out.insert('1.0', "The program cannot search for multiple words at a time. Please enter a single word with no spaces.")
    elif text not in m_word_data or text not in w_word_data:
        error_out.insert('1.0', f"{text} is not contained in the review data for both genders.")
    else:
        plot(canvas, m_word_data, w_word_data, text)


def handle_search(search_entry, search_out, m_word_data, w_word_data, search):
    """
    Called for <return> key in lower search field.
    Calls rmpdataanalysis.search_words() and displays results in GUI.
    Gets search target from given search_entry, puts results
    in given search_out text area.
    """
    target = search_entry.get().strip()
    if target:
        # Call the search_words function in rmpdataanalysis-solutions.py
        m_result = search_words(m_word_data, target)
        w_result = search_words(w_word_data, target)
        result = list(set(w_result) & set(m_result))
        out = ' '.join(result)
        search_out.delete('1.0', tkinter.END)
        search_out.insert('1.0', out)


def get_centered_x_coordinate(width, idx):
    """
    Given the width of the canvas and the index of the current review
    quality bucket to plot, returns the x coordinate of the centered
    location for the bars and label to be plotted relative to.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current label in the LABELS list
    Returns:
        x_coordinate (float): The centered x coordinate of the horizontal line 
                              associated with the specified label.
    """
    plot_width = width - LEFT_MARGIN - RIGHT_MARGIN

    # Calculate the center of the region for the label
    region_width = plot_width / len(LABELS)
    return LEFT_MARGIN + (idx + 0.5) * region_width


def draw_fixed_content(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background border and x-axis labels on it.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing content from the canvas
    width = canvas.winfo_width()    # get the width of the canvas
    height = canvas.winfo_height()  # get the height of the canvas
    # add your code here

    top_y = VERTICAL_MARGIN
    bottom_y = height - VERTICAL_MARGIN
    left_x = LEFT_MARGIN
    right_x = width - RIGHT_MARGIN

    # Draw the rectangle (plotting region) with a thicker line
    canvas.create_rectangle(left_x, top_y, right_x, bottom_y, width=LINE_WIDTH)

    # Draw the review quality labels ("Low Reviews", "Medium Reviews", "High Reviews")
    for i, label in enumerate(LABELS):
        x = get_centered_x_coordinate(width, i)
        y = bottom_y + LABEL_OFFSET  # Label slightly below the bottom line
        canvas.create_text(x, y, text=label, anchor=tkinter.N)


def get_bar_height(frequency, max_frequency, plot_height):
    """
    Given a frequency value and the maximum frequency, this function returns
    the height of the bar for the plotting area.

    Parameters:
    - frequency: The frequency value to plot
    - max_frequency: The maximum frequency in the dataset
    - plot_height: The height of the plotting area

    Returns:
    - The height of the bar relative to the plotting area
    """
    if max_frequency == 0:
        return 0
    return (frequency / max_frequency) * plot_height


def plot_word(canvas, m_word_data, w_word_data, word):
    """
    Given two dictionaries of word frequency data (one for men, one for women)
    and a single word, plots the distribution of the frequency of this word
    across gender and rating category.

    Input:
        canvas (tkinter Canvas): The canvas on which we are drawing.
        m_word_data (dictionary): Dictionary holding word frequency data for male professors.
        w_word_data (dictionary): Dictionary holding word frequency data for female professors.
        word (str): The word whose frequency distribution you want to plot.
    """

    draw_fixed_content(canvas)
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # Plotting region dimensions
    top_y = VERTICAL_MARGIN
    bottom_y = height - VERTICAL_MARGIN
    left_x = LEFT_MARGIN
    right_x = width - RIGHT_MARGIN
    plot_height = bottom_y - top_y

    # Get the data for the given word from each dictionary
    if word in m_word_data and word in w_word_data:
        m_data = m_word_data[word]
        w_data = w_word_data[word]
    else:
        # If the word is not found in either dictionary, return
        return

    # Calculate the maximum frequency from both datasets
    max_frequency = max(max(w_data), max(m_data))

    # Draw the Y-axis ticks and labels
    for i in range(NUM_VERTICAL_DIVISIONS + 1):
        tick_y = bottom_y - (i / NUM_VERTICAL_DIVISIONS) * plot_height
        frequency = int(i * max_frequency / NUM_VERTICAL_DIVISIONS)

        # Draw the tick mark and frequency label
        canvas.create_line(LEFT_MARGIN - TICK_WIDTH + 8, tick_y, LEFT_MARGIN, tick_y, width=LINE_WIDTH)
        canvas.create_text(LEFT_MARGIN - LABEL_OFFSET, tick_y, text=str(frequency), anchor=tkinter.E)

    # Draw the bars for each review category (Low, Medium, High)
    for i, label in enumerate(LABELS):
        # X coordinate for the center of the current label region
        center_x = get_centered_x_coordinate(width, i)

        # Calculate the bar heights for men and women
        w_height = get_bar_height(w_data[i], max_frequency, plot_height)
        m_height = get_bar_height(m_data[i], max_frequency, plot_height)

        # Draw the bar for women (left bar)
        w_top_y = bottom_y - w_height
        canvas.create_rectangle(center_x - BAR_WIDTH, w_top_y, center_x, bottom_y, fill='dodgerblue', width=LINE_WIDTH)

        # Draw the bar for men (right bar)
        m_top_y = bottom_y - m_height
        canvas.create_rectangle(center_x, m_top_y, center_x + BAR_WIDTH, bottom_y, fill='orange', width=LINE_WIDTH)

        # Draw gender labels at the top of the bars
        if w_data[i] > 0:
            canvas.create_text(center_x - BAR_WIDTH + TEXT_DX, w_top_y, text='W', anchor=tkinter.NW)
        if m_data[i] > 0:
            canvas.create_text(center_x + TEXT_DX, m_top_y, text='M', anchor=tkinter.NW)


def convert_counts_to_frequencies(word_data):
    """
    This function converts a dictionary
    of word counts into a dictionary of word frequencies by 
    dividing each count for a given gender by the total number 
    of words found in reviews about professors of that gender.
    """
    K = 1000000
    total_words = sum([sum(counts) for word, counts in word_data.items()])
    for word in word_data:
        gender_data = word_data[word]
        for i in range(3):
            gender_data[i] *= K / total_words


def main():
    import sys
    args = sys.argv[1:]
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    if len(args) == 2:
        WINDOW_WIDTH = int(args[0])
        WINDOW_HEIGHT = int(args[1])

    # Load data
    data = get_lines_from_file(FILENAME)
    # Get lines
    m_word_data = get_reviews_for_gender(data, 'M')
    w_word_data = get_reviews_for_gender(data, 'W')

    m_word_data = format_to_dict(m_word_data)
    w_word_data = format_to_dict(w_word_data)

    convert_counts_to_frequencies(m_word_data)
    convert_counts_to_frequencies(w_word_data)

    # Make window
    top = tkinter.Tk()
    top.wm_title('Rate My Professor Data Visualization')
    canvas = make_gui(top, WINDOW_WIDTH, WINDOW_HEIGHT, m_word_data, w_word_data, plot_word, search_words)

    # draw_fixed once at startup so we have the borders and labels
    # even before the user types anything.
    draw_fixed_content(canvas)

    # This needs to be called just once
    top.mainloop()


if __name__ == '__main__':
    main()

