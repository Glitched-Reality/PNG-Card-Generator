import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageTk, ImageFont
import textwrap
import os
import yaml

CONFIG_PATH = "card_config.yaml"

DEFAULT_CONFIG = {
    "border_styles": {
        "Basic": [150, 150, 150, 100, 100, 100],
        "Uncommon": [180, 255, 180, 0, 150, 0],
        "Rare": [180, 200, 255, 0, 80, 200],
        "Epic": [230, 200, 255, 100, 0, 100],
        "Legendary": [255, 230, 180, 180, 100, 0]
    },
    "gradient_types": {
        "Attack": [180, 60, 60, 220, 100, 100],
        "Defense": [60, 60, 180, 120, 120, 220],
        "Neutral": [120, 120, 120, 180, 180, 180],
        "Bounty": [180, 150, 80, 220, 190, 120]
    },
    "card_size": {
        "height": 900,
        "width": 600
    },
    "border_width": 10,
    "corner_radius": 25,
    "font_file": "C:/Windows/Fonts/arial.ttf",
    "font_title": 40,
    "font_desc": 28
}
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(DEFAULT_CONFIG, f, sort_keys=False)
    print("Default config file created.")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

BORDER_STYLES = {
    name: (tuple(values[:3]), tuple(values[3:]))
    for name, values in config["border_styles"].items()
}

GRADIENT_TYPES = {
    name: (tuple(values[:3]), tuple(values[3:]))
    for name, values in config["gradient_types"].items()
}


CARD_SIZE = (config["card_size"]["width"], config["card_size"]["height"])
BORDER_WIDTH = config["border_width"]
CORNER_RADIUS = config["corner_radius"]

icon_image = None
icon_color1 = None
icon_color2 = None

# Load font
FONT_PATH = config["font_file"]
text_color = (0, 0, 0, 255)

DEFAULT_FONT_PATH = "C:/Windows/Fonts/arial.ttf"

if os.path.exists(FONT_PATH):
    FONT_COMMAND = ImageFont.truetype(FONT_PATH, config["font_title"])
    FONT_DESC = ImageFont.truetype(FONT_PATH, config["font_desc"])
elif os.path.exists(DEFAULT_FONT_PATH):
    FONT_COMMAND = ImageFont.truetype(DEFAULT_FONT_PATH, config["font_title"])
    FONT_DESC = ImageFont.truetype(DEFAULT_FONT_PATH, config["font_desc"])
else:
    FONT_COMMAND = ImageFont.load_default()
    FONT_DESC = ImageFont.load_default()


def create_diagonal_gradient(size, start_color, end_color):
    width, height = size
    gradient = Image.new('RGB', size)
    pixels = gradient.load()
    for y in range(height):
        for x in range(width):
            t = (x + y) / (width + height - 2)
            r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
            pixels[x, y] = (r, g, b)
    return gradient

def generate_card_image(border_style, gradient_type, command_text, desc_text):
    border_light, border_dark = BORDER_STYLES[border_style]
    grad_dark, grad_light = GRADIENT_TYPES[gradient_type]

    # Create border gradient (light -> dark)
    border_gradient = create_diagonal_gradient(CARD_SIZE, border_light, border_dark).convert("RGBA")

    # Outer rounded mask
    outer_mask = Image.new("L", CARD_SIZE, 0)
    draw_outer = ImageDraw.Draw(outer_mask)
    draw_outer.rounded_rectangle([0, 0, CARD_SIZE[0], CARD_SIZE[1]], radius=CORNER_RADIUS, fill=255)

    # Inner gradient (dark -> light)
    inner_width = CARD_SIZE[0] - BORDER_WIDTH*2
    inner_height = CARD_SIZE[1] - BORDER_WIDTH*2
    inner_gradient = create_diagonal_gradient((inner_width, inner_height), grad_dark, grad_light).convert("RGBA")

    # Inner rounded mask
    inner_mask = Image.new("L", (inner_width, inner_height), 0)
    draw_inner = ImageDraw.Draw(inner_mask)
    draw_inner.rounded_rectangle([0, 0, inner_width, inner_height],
                                 radius=max(0, CORNER_RADIUS - BORDER_WIDTH),
                                 fill=255)

    # Paste inner gradient into border gradient
    border_gradient.paste(inner_gradient, (BORDER_WIDTH, BORDER_WIDTH), inner_mask)

    # Top section background gradient
    icon_height = int(inner_height / 4)
    top_bg_c1 = icon_color1 if icon_color1 else grad_dark
    top_bg_c2 = icon_color2 if icon_color2 else grad_light
    top_bg_gradient = create_diagonal_gradient((inner_width, icon_height), top_bg_c1, top_bg_c2).convert("RGBA")
    top_mask = Image.new("L", (inner_width, icon_height), 0)
    ImageDraw.Draw(top_mask).rectangle([0, 0, inner_width, icon_height], fill=255)
    # Composite top section onto inner gradient before masking
    inner_composite = inner_gradient.copy()
    inner_composite.paste(top_bg_gradient, (0, 0), top_mask)

    # Apply inner rounded mask
    inner_composite.putalpha(inner_mask)

    # Paste into border gradient
    border_gradient.paste(inner_composite, (BORDER_WIDTH, BORDER_WIDTH), inner_composite)

    # Draw dividing line
    line_y = BORDER_WIDTH + icon_height
    draw = ImageDraw.Draw(border_gradient)
    draw.line([(BORDER_WIDTH, line_y), (BORDER_WIDTH + inner_width, line_y)],
              fill=(0, 0, 0, 255), width=3)

    # Paste icon (unchanged colors)
    if icon_image:
        max_w = inner_width - 20
        max_h = icon_height - 10
        icon_w, icon_h = icon_image.size
        scale = min(max_w / icon_w, max_h / icon_h)
        new_size = (int(icon_w * scale), int(icon_h * scale))
        icon_resized = icon_image.resize(new_size, Image.LANCZOS)
        pos_x = BORDER_WIDTH + (inner_width - new_size[0]) // 2
        pos_y = BORDER_WIDTH + (icon_height - new_size[1]) // 2
        border_gradient.paste(icon_resized, (pos_x, pos_y), icon_resized)

    # Draw command text
    if command_text.strip():
        bbox = FONT_COMMAND.getbbox(command_text)
        w = bbox[2] - bbox[0]
        text_y = line_y + 5
        draw.text(((CARD_SIZE[0] - w) / 2, text_y), command_text, font=FONT_COMMAND, fill=text_color)
        desc_start_y = text_y + (bbox[3] - bbox[1]) + 15
    else:
        desc_start_y = line_y + 15

    # Draw description text
    desc_text = desc_entry.get("1.0", "end").strip()

    if desc_text:
        draw.multiline_text(
            (BORDER_WIDTH + 5, desc_start_y),
            desc_text,
            font=FONT_DESC,
            fill=text_color,
            spacing=4
        )

    # Apply outer rounded mask
    border_gradient.putalpha(outer_mask)

    return border_gradient

def update_preview():
    img = generate_card_image(
        border_var.get(),
        gradient_var.get(),
        command_entry.get(),
        desc_entry.get("1.0", tk.END).strip()
    )

    # Resize image to fixed preview size (300x450)
    preview_size = (300, 450)
    img_resized = img.resize(preview_size, Image.LANCZOS)

    tk_img = ImageTk.PhotoImage(img_resized)
    preview_label.config(image=tk_img)
    preview_label.image = tk_img


def pick_text_color():
    global text_color
    color = colorchooser.askcolor(title="Pick Text Color")
    if color[0]:
        text_color = tuple(map(int, color[0])) + (255,)  # Add alpha channel
    schedule_update()


# Debounce wrapper
update_job = None
def schedule_update(*args):
    global update_job
    if update_job:
        root.after_cancel(update_job)
    update_job = root.after(300, update_preview)

def save_card():
    spath = "card_output"
    if not os.path.exists(spath):
        os.makedirs(spath)
    img = generate_card_image(
        border_var.get(),
        gradient_var.get(),
        command_entry.get(),
        desc_entry.get("1.0", tk.END).strip()
    )
    filename = f"{spath}/{border_var.get().lower()}_{gradient_var.get().lower()}_{command_entry.get().strip().lower().replace(" ", "_")}.png"
    img.save(filename)
    print(f"Saved {filename}")

def load_icon():
    global icon_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path).convert("RGBA")
        icon_image = img
        schedule_update()

def pick_icon_color1():
    global icon_color1
    color = colorchooser.askcolor(title="Pick Top Section Color 1")
    if color[0]:
        icon_color1 = tuple(map(int, color[0]))
    schedule_update()

def pick_icon_color2():
    global icon_color2
    color = colorchooser.askcolor(title="Pick Top Section Color 2")
    if color[0]:
        icon_color2 = tuple(map(int, color[0]))
    schedule_update()

# GUI Setup
root = tk.Tk()
root.title("PNG Card Generator")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

controls_frame = tk.Frame(main_frame)
controls_frame.pack(side="left", fill="y", padx=10, pady=10)

preview_frame = tk.Frame(main_frame)
preview_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Controls
tk.Label(controls_frame, text="Select Border Style:").pack(pady=5)
border_var = tk.StringVar(value=list(BORDER_STYLES.keys())[0])
tk.OptionMenu(controls_frame, border_var, *BORDER_STYLES.keys()).pack()

tk.Label(controls_frame, text="Select Gradient Type:").pack(pady=5)
gradient_var = tk.StringVar(value=list(GRADIENT_TYPES.keys())[0])

tk.OptionMenu(controls_frame, gradient_var, *GRADIENT_TYPES.keys()).pack()

tk.Label(controls_frame, text="Title Text:").pack(pady=5)
command_entry = tk.Entry(controls_frame)
command_entry.pack(fill="x")

tk.Label(controls_frame, text="Description:").pack(pady=5)
desc_entry = tk.Text(controls_frame, height=5, wrap="word")
desc_entry.pack(fill="x")

tk.Button(controls_frame, text="Pick Text Color", command=pick_text_color).pack(pady=2)

tk.Button(controls_frame, text="Load Icon", command=load_icon).pack(pady=5)
tk.Button(controls_frame, text="Pick Top Section Color 1", command=pick_icon_color1).pack(pady=2)
tk.Button(controls_frame, text="Pick Top Section Color 2", command=pick_icon_color2).pack(pady=2)

tk.Button(controls_frame, text="Save Card", command=save_card).pack(pady=10)

# Bind updates with debounce
border_var.trace_add("write", schedule_update)
gradient_var.trace_add("write", schedule_update)
command_entry.bind("<KeyRelease>", schedule_update)
desc_entry.bind("<KeyRelease>", schedule_update)

# Preview area
preview_label = tk.Label(preview_frame)
preview_label.pack(expand=True)

# Initial preview
update_preview()

root.mainloop()
