from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configuration
text_list = [
    "Hello world",
    "main.py"
]

output_video = "text_slideshow.mp4"
image_size = (1280, 720)
background_color = (30, 30, 30)
text_color = (255, 255, 255)
font_path = "arial.ttf"  # Update this if Arial is not available
frame_duration = 10  # Duration per slide (seconds)
max_font_size = 40  # Maximum font size to try

def create_text_image(text, size, background, text_color, font_path):
    """Creates an image with the text centered and wrapped to fit the frame."""
    img = Image.new("RGB", size, background)
    draw = ImageDraw.Draw(img)

    # Try different font sizes until the text fits within the image
    for font_size in range(max_font_size, 10, -2):  # Decrease font size if needed
        font = ImageFont.truetype(font_path, font_size)
        wrapped_text = wrap_text(text, draw, font, size[0] - 40)  # Wrap text

        # Calculate total height to center the text vertically
        text_height = sum(draw.textsize(line, font=font)[1] for line in wrapped_text)
        if text_height <= size[1] - 40:  # Check if text fits
            break

    # Center the text
    y = (size[1] - text_height) // 2  # Center vertically
    for line in wrapped_text:
        text_width, _ = draw.textsize(line, font=font)
        x = (size[0] - text_width) // 2  # Center horizontally
        draw.text((x, y), line, font=font, fill=text_color)
        y += font_size + 5  # Line spacing

    return img

def wrap_text(text, draw, font, max_width):
    """Wraps text so that it fits within the given width."""
    lines = []
    for paragraph in text.split("\n"):
        wrapped_lines = textwrap.wrap(paragraph, width=50)  # Wrap text into lines
        for line in wrapped_lines:
            if draw.textsize(line, font=font)[0] <= max_width:
                lines.append(line)
            else:
                # Split longer words if necessary
                words = line.split()
                temp_line = ""
                for word in words:
                    if draw.textsize(temp_line + word, font=font)[0] <= max_width:
                        temp_line += word + " "
                    else:
                        lines.append(temp_line.strip())
                        temp_line = word + " "
                lines.append(temp_line.strip())
    return lines

# Generate images with text
image_files = []
for i, text in enumerate(text_list):
    img = create_text_image(text, image_size, background_color, text_color, font_path)
    image_file = f"frame_{i}.png"
    img.save(image_file)
    image_files.append(image_file)

# Create video from the images
clips = [ImageClip(img).set_duration(frame_duration) for img in image_files]
video = concatenate_videoclips(clips, method="compose")

# Set background music
audio = AudioFileClip("bg.mp3")
video = video.set_audio(audio)

# Export the video
video.write_videofile(output_video, fps=24)

# Clean up temporary image files
import os
for img in image_files:
    os.remove(img)

print(f"Video saved as {output_video}")
