# A5.py
# CS 1400
# Assignment 5: Image Processing
# Written by David Johnson, Noelle Brown, and Shaan Luthra

from graphics import *
from random import randint, random


# Make a new image that moves the red intensity value of a pixel in the original image
# to the green part of a pixel, moves the green value to blue,
# and the blue value to red. An image that had a bright red part will end up with
# that part being bright green in the new image.
#
# Study the pattern of the loop inside a loop (called nested loops). Each time the first loop
# does a single repeat, the entire inner loop does all its repetitions.
#
# Look how to get the color at a pixel, change the color, and set the pixel to the new color.
# The assignment problems below will use these steps.
# This function returns a new image with changed colors. The code in main calls
# this function and draws the returned new image.
def switch_image_colors(image):
    """Return a copy of the image with R->G, G->B, B->R rotation."""
    switched_image = image.clone()
    w = image.getWidth()
    h = image.getHeight()
    for y in range(h):
        for x in range(w):
            color = image.getPixel(x, y)
            new_color = [color[2], color[0], color[1]]
            switched_image.setPixel(x, y, new_color)
    return switched_image


# ========== Assignment functions to implement ==========

def color_image_to_gray_scale(image):
    """
    Convert the input image to grayscale using luminance:
    gray = int(0.299*R + 0.587*G + 0.114*B)
    Returns a cloned image with each pixel set to [gray, gray, gray].
    """
    gray_img = image.clone()
    w = image.getWidth()
    h = image.getHeight()
    for y in range(h):
        for x in range(w):
            r, g, b = image.getPixel(x, y)
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray_img.setPixel(x, y, [gray, gray, gray])
    return gray_img


def color_image_to_black_and_white(image, threshold):
    """
    Convert the image to pure black and white using a luminance threshold.
    First computes grayscale luminance per pixel, then sets pixel to
    white [255,255,255] if luminance >= threshold, else black [0,0,0].
    """
    # We can reuse the grayscale logic in place, but spec asks to convert then threshold.
    bw_img = image.clone()
    w = image.getWidth()
    h = image.getHeight()
    for y in range(h):
        for x in range(w):
            r, g, b = image.getPixel(x, y)
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            if gray >= threshold:
                bw_img.setPixel(x, y, [255, 255, 255])
            else:
                bw_img.setPixel(x, y, [0, 0, 0])
    return bw_img


def sepia_image(image):
    """
    Produce a sepia-toned image using the classic transform:
    newR = 0.393*R + 0.769*G + 0.189*B
    newG = 0.349*R + 0.686*G + 0.168*B
    newB = 0.272*R + 0.534*G + 0.131*B
    If any new channel > 255, set it to 255 (use if-statements as requested).
    """
    sepia_img = image.clone()
    w = image.getWidth()
    h = image.getHeight()
    for y in range(h):
        for x in range(w):
            R, G, B = image.getPixel(x, y)
            newR = int(0.393 * R + 0.769 * G + 0.189 * B)
            newG = int(0.349 * R + 0.686 * G + 0.168 * B)
            newB = int(0.272 * R + 0.534 * G + 0.131 * B)

            # Use if statements to clamp to 255 if necessary (assignment requirement)
            if newR > 255:
                newR = 255
            if newG > 255:
                newG = 255
            if newB > 255:
                newB = 255

            sepia_img.setPixel(x, y, [newR, newG, newB])
    return sepia_img


def rainbow_gradient(image):
    """
    Apply a vertical rainbow-style gradient blended with original pixel colors.
    For each pixel compute GradientRatio = y / imageHeight (0 at top, 1 at bottom)
    and set:
        newR = int(R * (1 - GradientRatio))
        newG = int(G * (1 - abs(2*GradientRatio - 1)))
        newB = int(B * GradientRatio)
    Returns a cloned image with these adjusted colors.
    """
    out = image.clone()
    w = image.getWidth()
    h = image.getHeight()
    # Avoid dividing by zero for tiny images
    height = float(h) if h > 0 else 1.0
    for y in range(h):
        grad = y / height  # ratio between 0 (top) and <1 (bottom)
        for x in range(w):
            R, G, B = image.getPixel(x, y)
            newR = int(R * (1 - grad))
            newG = int(G * (1 - abs(2 * grad - 1)))
            newB = int(B * grad)
            out.setPixel(x, y, [newR, newG, newB])
    return out


def custom_filter(image):
    """
    Apply a custom color filter that tints the image toward teal and
    slightly increases contrast. This keeps the image recognizable but
    changes its color mood. (You can tweak the constants to taste.)
    """
    out = image.clone()
    w = image.getWidth()
    h = image.getHeight()
    for y in range(h):
        for x in range(w):
            r, g, b = image.getPixel(x, y)

            # Slight contrast boost around mid-gray: move values away from 128
            def boost(channel):
                if channel > 128:
                    return int(min(255, 128 + (channel - 128) * 1.15))
                else:
                    return int(max(0, 128 - (128 - channel) * 1.15))

            br = boost(r)
            bg = boost(g)
            bb = boost(b)

            # Apply teal tint: reduce red a bit, boost blue and green slightly
            newR = int(br * 0.85)
            newG = int(bg * 1.05)
            newB = int(bb * 1.10)

            # Clamp using graphics.clamp helper (safe, but keep values in 0-255)
            newR = clamp(newR)
            newG = clamp(newG)
            newB = clamp(newB)

            out.setPixel(x, y, [newR, newG, newB])
    return out


def green_screen_image(foreground, background):
    """
    Merge a foreground image shot on a pure green screen with a background.
    For each pixel: if the foreground pixel is pure green [0,255,0], use the
    background pixel; otherwise use the foreground pixel. The foreground is
    centered on the background.
    """
    merged = background.clone()
    bg_w = merged.getWidth()
    bg_h = merged.getHeight()
    fg_w = foreground.getWidth()
    fg_h = foreground.getHeight()

    offset_x = (bg_w - fg_w) // 2
    offset_y = (bg_h - fg_h) // 2

    for y in range(fg_h):
        for x in range(fg_w):
            fr, fg_c, fb = foreground.getPixel(x, y)
            bx = x + offset_x
            by = y + offset_y
            if 0 <= bx < bg_w and 0 <= by < bg_h:
                # If pixel is exactly pure green, use background pixel (leave merged as is)
                if fr == 0 and fg_c == 255 and fb == 0:
                    # leave merged pixel as background pixel (already present)
                    pass
                else:
                    # otherwise copy the foreground pixel into merged
                    merged.setPixel(bx, by, [fr, fg_c, fb])
    return merged


def color_image_to_pointillist(image, win, num_points):
    """
    Create a pointillist rendering by repeatedly sampling a random pixel from the image
    and drawing a filled circle at that location with the pixel's color.
    The function draws directly to the provided GraphWin and returns None.
    """
    w = image.getWidth()
    h = image.getHeight()

    # Choose a reasonable radius based on image size (small relative to image)
    # Use at least 1 so dots are visible
    radius = max(1, int(max(w, h) / 200))

    # Draw num_points circles. Update the window occasionally for responsiveness.
    update_interval = max(1, num_points // 50)  # roughly 50 flushes during drawing
    for i in range(num_points):
        x = randint(0, w - 1)
        y = randint(0, h - 1)
        r, g, b = image.getPixel(x, y)
        circ = Circle(Point(x, y), radius)
        # setFill accepts either a color string or RGB triple
        circ.setFill(r, g, b)
        circ.setWidth(0)
        circ.draw(win)
        if (i + 1) % update_interval == 0:
            # flush a bit so the window doesn't freeze
            win.flush()
    win.flush()
    return None


# ========== Helper load and main ==========

def load_image(filename):
    """Load an image file and center it (same helper from starter)."""
    image = Image(Point(0, 0), filename)
    image.move(int(image.getWidth() / 2), int(image.getHeight() / 2))
    return image


def main():
    # Load images (make sure Arches.png and green-screen-cat.png exist in your project)
    arches_image = load_image("Arches.png")
    cat_image = load_image("green-screen-cat.png")

    # Create window sized to the arches image (you can change this if you like)
    win = GraphWin('Image Art', arches_image.getWidth(), arches_image.getHeight(), autoflush=False)

    # Show original and step through each effect with mouse clicks.
    # Comment/uncomment the blocks below while developing to save time.
    arches_image.draw(win)
    win.getMouse()

    # swap colors example (provided)
    switched_image = switch_image_colors(arches_image)
    switched_image.draw(win)
    win.getMouse()

    # grayscale
    gray_image = color_image_to_gray_scale(arches_image)
    gray_image.draw(win)
    gray_image.save("gray.png")
    win.getMouse()

    # black & white with threshold 100 (example)
    bw_image = color_image_to_black_and_white(arches_image, 100)
    bw_image.draw(win)
    bw_image.save("bw.png")
    win.getMouse()

    # sepia
    sep = sepia_image(arches_image)
    sep.draw(win)
    sep.save("sepia.png")
    win.getMouse()

    # rainbow
    rainbow = rainbow_gradient(arches_image)
    rainbow.draw(win)
    rainbow.save("rainbow.png")
    win.getMouse()

    # custom filter
    custom = custom_filter(arches_image)
    custom.draw(win)
    custom.save("custom.png")
    win.getMouse()

    # green screen merge (foreground cat over arches)
    merged = green_screen_image(cat_image, arches_image)
    merged.draw(win)
    merged.save("merged.png")
    win.getMouse()

    # pointillist: draws many circles. Use 25000 for submission capture, but you can test with fewer.
    color_image_to_pointillist(arches_image, win, 25000)
    win.getMouse()

    win.close()


if __name__ == "__main__":
    main()
