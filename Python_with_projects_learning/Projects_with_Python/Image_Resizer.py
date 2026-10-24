
from PIL import Image
from tkinter import Tk, filedialog, simpledialog, messagebox
import os
import io

root = Tk()
root.withdraw()

try:
    # Step 1: Select image
    image_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp"),
            ("All files", "*.*")
        ]
    )

    if not image_path:
        print("No image selected.")
        raise SystemExit

    image = Image.open(image_path)
    print("Original dimensions:", image.size)

    original_kb = os.path.getsize(image_path) / 1024
    print(f"Original file size: {original_kb:.2f} KB")

    # Step 2: Enter new dimensions
    width = simpledialog.askinteger(
        "Image Resizer", "Enter width in pixels:", minvalue=1
    )
    if width is None:
        raise SystemExit

    height = simpledialog.askinteger(
        "Image Resizer", "Enter height in pixels:", minvalue=1
    )
    if height is None:
        raise SystemExit

    # Step 3: Enter target file size
    target_kb = simpledialog.askinteger(
        "Image Resizer",
        "Enter target file size in KB:",
        minvalue=1
    )
    if target_kb is None:
        raise SystemExit

    target_bytes = target_kb * 1024

    # Step 4: Resize dimensions
    resized = image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    # JPEG does not support transparency
    if resized.mode not in ("RGB", "L"):
        resized = resized.convert("RGB")

    # Step 5: Compress to try to reach target KB
    output = io.BytesIO()
    quality = 95

    while quality >= 5:
        output = io.BytesIO()

        resized.save(
            output,
            format="JPEG",
            quality=quality,
            optimize=True
        )

        if output.tell() <= target_bytes:
            break

        quality -= 5

    # Step 6: Save output
    folder = os.path.dirname(image_path)
    name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(folder, name + "_resized.jpg")

    with open(output_path, "wb") as file:
        file.write(output.getvalue())

    final_kb = os.path.getsize(output_path) / 1024

    print("New dimensions:", resized.size)
    print(f"Final file size: {final_kb:.2f} KB")
    print("Saved to:", output_path)

    if final_kb <= target_kb:
        result = "Target file size achieved!"
    else:
        result = (
            "Target size could not be reached at the selected "
            "dimensions, even with strong compression."
        )

    messagebox.showinfo(
        "Image Resizer",
        f"Original size: {original_kb:.2f} KB\n"
        f"Final size: {final_kb:.2f} KB\n"
        f"Dimensions: {width} x {height}\n\n"
        f"{result}\n\nSaved to:\n{output_path}"
    )

except Exception as error:
    messagebox.showerror("Error", str(error))

finally:
    root.destroy()
