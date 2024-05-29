from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


# Initialize the Tkinter window
root = Tk()
root.title("Image Watermarking App")
root.geometry("800x600")

# Global variable to hold the image
img = None
watermarked_display = None
image_watermark_added = None
watermark_image_copy = None
# image_watermark_added == False
# original_size = None

# Function to open image
def open_image():
    global img, original_size
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        img = Image.open(file_path)
        original_size = img.size
        img_copy = img.copy()
        img_copy.thumbnail((400, 400))
        img_tk = ImageTk.PhotoImage(img_copy)
        canvas.create_image(200, 200, image=img_tk)
        canvas.image = img_tk

# Function to add text watermark
def add_text_watermark():
    global img, image_path, image_label, watermarked_display, image_watermark_added
    if img is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    # watermark_text = "Sample Watermark"
    watermark_text = text_entry.get()
    # opacity = opacity_scale.get()

    # Determine the appropriate font size based on image width
    width, height = img.size
    font_size = int(width * 0.08)  # Calculate font size as 8% of image width
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)

    # Create a transparent image for the text
    text_image = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)


    # Get the size of the text
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Calculate the position for the watermark
    width, height = img.size
    x = (width - textwidth) / 2
    y = (height - textheight) / 2

    # Get the opacity value from the scale widget
    opacity = opacity_scale.get()
    alpha = int(255 * (opacity / 100))

    # Add the text watermark
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, alpha))

    # Composite the text image onto the original image
    watermarked_display = Image.alpha_composite(img.convert("RGBA"), text_image)

    # Create a scaled-down copy for preview (not affecting the original)
    preview_image = watermarked_display.copy()
    preview_image.thumbnail((400, 400))

    # Convert the watermarked image for display
    img_display = ImageTk.PhotoImage(preview_image)

    # Update the canvas to show the watermarked image
    canvas.create_image(200, 200, image=img_display)
    canvas.image = img_display

    # text_watermark_added = True
    image_watermark_added = False

# Function to add image watermark
def add_watermark():
    global img, image_path, image_label, watermarked_display, image_watermark_added, watermark_image_copy

    print(f"image watermark added: {image_watermark_added}")
    if img is None:
        messagebox.showwarning("No image", "Please upload an image first.")
        return
    if image_watermark_added != True:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.svg")])
        if not file_path:
            return
        watermark_image = Image.open(file_path).convert("RGBA")
        watermark_image_copy = watermark_image.copy()
    else:
        watermark_image = watermark_image_copy

     # Resize the watermark image to fit 20% of the original image width
    width, height = img.size
    watermark_width = int(width * 0.2)
    aspect_ratio = watermark_image.width / watermark_image.height
    watermark_height = int(watermark_width / aspect_ratio)

    # Resize the watermark image
    watermark_image = watermark_image.resize((watermark_width, watermark_height), Image.LANCZOS)

    # Get the opacity value from the scale widget
    opacity = opacity_scale.get()
    alpha = int(255 * (opacity / 100))

    # Apply opacity to the watermark image
    watermark_image = watermark_image.copy()
    for x in range(watermark_width):
        for y in range(watermark_height):
            r, g, b, a = watermark_image.getpixel((x, y))
            watermark_image.putpixel((x, y), (r, g, b, int(a * (alpha / 255))))

   # Create a transparent layer the size of the image to place the watermark on
    transparent = Image.new('RGBA', img.size, (0, 0, 0, 0))

    # Position the watermark at the bottom right corner
    x = width - watermark_width - 10
    y = height - watermark_height - 10

    # Paste the watermark image onto the transparent layer
    transparent.paste(watermark_image, (x, y), watermark_image)

    # Composite the original image with the transparent layer
    watermarked_display = Image.alpha_composite(img.convert("RGBA"), transparent)

    # Convert the watermarked image for display
    img_copy = watermarked_display.copy()
    img_copy.thumbnail((400, 400))
    img_display = ImageTk.PhotoImage(img_copy)

    # Update the canvas to show the watermarked image
    canvas.create_image(200, 200, image=img_display)
    canvas.image = img_display

    image_watermark_added = True

# Function to save watermark
def save_image():
    global watermarked_display, original_size
    if watermarked_display is None:
        messagebox.showerror("Error", "No watermarked image to save. Please add a watermark first.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        # Convert RGBA image to RGB
        rgb_image = watermarked_display.convert("RGB")
        # # Resize the watermarked image to match the original size
        # resized_image = rgb_image.resize(original_size)
        rgb_image.save(file_path)
        messagebox.showinfo("Success", f"Image saved to {file_path}")

def on_opacity_change(value):
    global img, image_watermark_added, root
    # if root:
    if img is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return
    print(value)
    # opacity = value
    if image_watermark_added == True:
        add_watermark()
    else:
        add_text_watermark()  # Call add_text_watermark with the new opacity





# Canvas to display the image
canvas = Canvas(root, width=400, height=400)
canvas.pack()

# Button to upload an image
upload_btn = Button(root, text="Upload Image", command=open_image)
upload_btn.pack()

# Entry to input watermark text
text_entry = Entry(root)
text_entry.pack()

# Button to add text watermark
watermark_btn = Button(root, text="Add Text Watermark", command=add_text_watermark)
watermark_btn.pack()

# Button to add watermark
watermark_btn = Button(root, text="Add Watermark", command=add_watermark)
watermark_btn.pack()

# Add the "Save Image" button
save_btn = Button(root, text="Save Image", command=save_image)
save_btn.pack()

opacity_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL)
# Temporarily unregister the command
opacity_scale.config(command=None)
opacity_scale.set(100)
# Re-register the command
opacity_scale.config(command=on_opacity_change)
opacity_scale.pack()
# opacity_scale.bind("<Motion>", add_text_watermark)

# Add a label to display the image
image_label = Label(root)
image_label.pack()

root.mainloop()