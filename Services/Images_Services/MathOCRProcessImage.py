from PIL import Image


def math_ocr_process_image(thread_id, filename, model, latex_outputs):
    img = Image.open(filename)  # Open the image file
    latex_output = model(img)  # Run the Math OCR Model (pix2tex) on the image
    formatted_latex_output = ''.join(latex_output)  # Join latex fragments into a single string
    latex_outputs[filename] = formatted_latex_output  # Save the LaTeX output in the dictionary
    # print(f"Thread {thread_id}: LaTeX output for {filename}: {formatted_latex_output}")
