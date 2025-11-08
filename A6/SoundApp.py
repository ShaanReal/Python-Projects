import time
import random
import math
import Audio
from Audio import *
import wave
import turtle
import tkinter as tk
from tkinter import filedialog

from SoundTools import *

# Sound Editor GUI
# Written by David E. Johnson for U of Utah
# This code should not be changed for the assignment.


class FastSampleTrace:
    def __init__(self, canvas):
        self.tscreen = turtle.TurtleScreen(canvas)
        self.t = turtle.RawTurtle(self.tscreen)
        self.t.speed(0)
        self.t.hideturtle()
        self.t.penup()

    def drawSamples(self, new_samples, original_samples, vertical_scale):
        self.t.clear()
        (w,h) = self.tscreen.screensize()
        self.t.penup()

        self.tscreen.tracer(False)
        if new_samples:
            self.t.pencolor("red")
            self.t.goto(-w//2, h//4 + new_samples[0]//vertical_scale)
            self.t.pendown()
            for index in range(len(new_samples)):
                self.t.goto(index-w//2, h//4 + new_samples[index]//vertical_scale)

        if original_samples:
            self.t.penup()
            self.t.goto(-w//2, -h//4 + original_samples[0]//vertical_scale)
            self.t.pencolor("black")
            self.t.pendown()
            for index in range(len(original_samples)):
                self.t.goto(index-w//2, -h//4 + original_samples[index]//vertical_scale)

        self.tscreen.update()
        self.t.penup()


class SoundApp:
    def __init__(self):
        root = tk.Tk()
        root.title("Sound Editor")
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT)

        self.load_file("asyouwish2.wav")
        self.canvas = turtle.ScrolledCanvas(self.frame, 500, 500, len(self.original_samples)+5000, 500)
        self.canvas.pack()
        self.sample_viewer = FastSampleTrace(self.canvas)

        self.side_frame = tk.Frame(root)
        self.add_buttons(self.side_frame)
        self.side_frame.pack(side=tk.RIGHT)
        self.sample_viewer.drawSamples(self.original_samples, self.original_samples, 300)
        tk.mainloop()

    def load_file(self, filename):
        """A sound file is a list of samples and the rate they get played."""
        sound_data = [0, 0]            # an "empty" list
        read_wav(filename, sound_data) # get data INTO sound_data
        self.original_samples = [val + 2000 for val in sound_data[0]]
        self.original_sample_rate = sound_data[1]

    def play(self, samples, sample_rate):
        """This plays whatever is loaded into samples at sample_rate speed"""
        sound_data = [samples, sample_rate]
        write_wav(sound_data, "out.wav") # write data to out.wav
        play('out.wav')

    def play_and_visualize(self):
        self.play(self.original_samples, self.original_sample_rate)
        self.sample_viewer.drawSamples(self.original_samples, self.original_samples, 300)

    def louder_and_visualize(self):
        new_samples = make_louder_samples(self.original_samples, 5.0)
        self.play(new_samples, self.original_sample_rate)
        self.sample_viewer.drawSamples(new_samples, self.original_samples, 300)

    def quicken_and_visualize(self):
        self.play(self.original_samples, self.original_sample_rate * 1.5)
        self.sample_viewer.drawSamples(self.original_samples, self.original_samples, 300)

    def make_echo_and_visualize(self):
        new_samples = make_echo_samples(self.original_samples, 5000, 0.25)
        self.play(new_samples, self.original_sample_rate)
        self.sample_viewer.drawSamples(new_samples, self.original_samples, 300)

    def make_clipped_samples_and_visualize(self):
        boosted_samples = [val*1 for val in self.original_samples]
        new_samples = make_clipped_samples(boosted_samples, 5000)
        print(self.original_samples)
#        print(new_samples)
        self.play(new_samples, self.original_sample_rate)
        self.sample_viewer.drawSamples(new_samples, self.original_samples, 300)

    def make_reversed_samples_and_visualize(self):
        new_samples = make_reversed_samples(self.original_samples)
        self.play(new_samples, self.original_sample_rate)
        self.sample_viewer.drawSamples(new_samples, self.original_samples, 300)

    def make_noisy_samples_and_visualize(self):
        new_samples = make_noisy_samples(self.original_samples, 2000)
        self.play(new_samples, self.original_sample_rate)
        self.sample_viewer.drawSamples(new_samples, self.original_samples, 300)

    def make_smoothed_samples_and_visualize(self):
        new_samples = make_smoothed_samples(self.original_samples)
        self.play(new_samples, self.original_sample_rate)
        self.sample_viewer.drawSamples(new_samples, self.original_samples, 300)

    def add_buttons(self, button_frame):

        speed_button = tk.Button(button_frame,
                       text="Chipmunk",
                       fg="red",
                       command= self.quicken_and_visualize)
        speed_button.pack(side=tk.TOP)

        reversed_button = tk.Button(button_frame,
                       text="Reversed",
                       fg="red",
                       command = self.make_reversed_samples_and_visualize)
        reversed_button.pack(side=tk.TOP)

        louder_button = tk.Button(button_frame,
                       text="Louder",
                       fg="red",
                       command = self.louder_and_visualize)
        louder_button.pack(side=tk.TOP)

        clip_button = tk.Button(button_frame,
                       text="Clip",
                       fg="red",
                       command = self.make_clipped_samples_and_visualize)
        clip_button.pack(side=tk.TOP)

        noise_button = tk.Button(button_frame,
                       text="Add Noise",
                       fg="red",
                       command = self.make_noisy_samples_and_visualize)
        noise_button.pack(side=tk.TOP)

        smooth_button = tk.Button(button_frame,
                       text="Reduce Noise",
                       fg="red",
                       command = self.make_smoothed_samples_and_visualize)
        smooth_button.pack(side=tk.TOP)

        echo_button = tk.Button(button_frame,
                       text="Add Echo",
                       fg="red",
                       command = self.make_echo_and_visualize)
        echo_button.pack(side=tk.TOP)

        pbutton = tk.Button(button_frame,
                       text="Play",
                       fg="red",
                       command = self.play_and_visualize)
        pbutton.pack(side=tk.TOP)

        qbutton = tk.Button(button_frame,
                       text="Quit",
                       fg="red",
                       command=quit)
        qbutton.pack(side=tk.TOP)





def main():
    app = SoundApp()

if __name__ == "__main__":
    main()
