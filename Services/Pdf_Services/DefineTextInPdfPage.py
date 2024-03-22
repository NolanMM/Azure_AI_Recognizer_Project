from Services.coherence_checker import is_coherent
from Services.Images_Services.ProcessImage import process_image
import easyocr
import threading
import cv2


def define_text_in_pdf_page(image_page_path, page_number, output_folder):
    text_list = []  # Text list to store all the text in the page with coordinates inside the page
    math_formula_latex_with_coordinates = []

    image_page = cv2.imread(image_page_path)
    reader = easyocr.Reader(['en'], gpu=True, quantize=True)
    result = reader.readtext(image_page)
    # is_contain_math = False
    # math_pattern = (
    #     r'\b(?:(?:[0,1,2,3,4,5,6,7,8,9]+(?:\.[0,1,2,3,4,5,6,7,8,9]*)?|\.[0,1,2,3,4,5,6,7,8,9]+)(?:[eE][+-]?['
    #     r'0-9]+)?|pi|π|e|inf|infty|∞|sqrt|log|ln|sin|cos|tan|cot|sec|csc)\b|[\(\)\[\]\{\}+\-*/\^=,]')
    for detection in result:
        text = detection[1]
        if not is_coherent(text):
            math_formula_latex_with_coordinates = process_image(threading.current_thread().ident, image_page_path,
                                                                page_number, output_folder)
            break
        text_coordinates = detection[0]
        x, y = text_coordinates[0][0], text_coordinates[0][1]
        text_list.append((page_number, (x, y), text))

    return text_list, math_formula_latex_with_coordinates


def process_page(page_path, page_number, output_folder, results):
    # thread_id = threading.current_thread().ident
    text_list, math_formula_latex_with_coordinates = define_text_in_pdf_page(page_path, page_number, output_folder)

    # Merge text and math formulas based on their coordinates
    merged_items = sorted(text_list + math_formula_latex_with_coordinates, key=lambda item: item[1][1])

    # Remove coordinates from text items
    processed_items = [(item[0], item[2]) if len(item) == 3 else (item[0], item[3]) for item in merged_items]

    results[page_number] = processed_items
