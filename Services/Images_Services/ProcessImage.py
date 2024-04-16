from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient, AnalysisFeature
from pix2tex.cli import LatexOCR
from Services.Images_Services.ScreenshotMath import screenshot_math
from Services.Images_Services.MathOCRProcessImage import math_ocr_process_image
import os


def format_polygon(polygon):
    if not polygon:
        return "N/A"
    coordinate = ", ".join([f"[{p.x}, {p.y}]" for p in polygon])
    pairs = coordinate.split('], [')
    coordinates_list_tuple = [(float(pair.strip('][').split(', ')[0]), float(pair.strip('][').split(', ')[1])) for pair
                              in pairs]
    return coordinates_list_tuple


def process_image(thread_id, image_path, page_number, user_folder):
    math_text_coordinates = []  # Text list to store all the text in the page with coordinates inside the page
    text_list = []  # Text list to store all the text in the page with coordinates inside the page
    endpoint = "https://nolanm-document-intelligence.cognitiveservices.azure.com/"
    key = "17912dc741e34f12aa266b7edc34fb52"

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-layout", document=f, features=[AnalysisFeature.FORMULAS]
        )
    result = poller.result()
    for page in result.pages:
        output_folder_page = os.path.join(user_folder, f"{page_number}_pages")
        output_folder_formula = os.path.join(output_folder_page, "_formulas")
        if not os.path.exists(output_folder_formula):
            os.makedirs(output_folder_formula)
        page_width = page.width
        page_height = page.height
        list_formulas = [f for f in page.formulas]

        for formula_idx, formula in enumerate(list_formulas):
            save_image = screenshot_math(format_polygon(formula.polygon), output_folder_formula, formula_idx,
                                         image_path)
            fomular_coordinates = format_polygon(formula.polygon)
            coordinates = [(int(x), int(y)) for x, y in fomular_coordinates]
            x_coords = [pt[0] for pt in coordinates]
            y_coords = [pt[1] for pt in coordinates]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            top_left = (x_min, y_min)
            bottom_right = (x_max, y_max)
            if save_image:
                model = LatexOCR()  # Initialize the LatexOCR model
                latex_outputs = {}
                output_path = os.path.join(output_folder_formula, f"{formula_idx + 1}.png")
                math_ocr_process_image(thread_id, output_path, model, latex_outputs)
                full_latex_formula = latex_outputs[output_path]  # Get the formatted latex formula
                math_text_coordinates.append(
                    (page_number, top_left, bottom_right, full_latex_formula))  # Append to list
                print("Image saved")
    return math_text_coordinates
