import cv2
import os


def screenshot_math(coordinates, output_folder, formula_idx, image_path):
    try:
        coordinates = [(int(x), int(y)) for x, y in coordinates]
        x_coords = [pt[0] for pt in coordinates]
        y_coords = [pt[1] for pt in coordinates]
        x_min, x_max = min(x_coords) - 6, max(x_coords) + 6
        y_min, y_max = min(y_coords) - 6, max(y_coords) + 6
        image_page = cv2.imread(image_path)
        cropped_image = image_page[y_min:y_max, x_min:x_max]
        output_path = os.path.join(output_folder, f"{formula_idx + 1}.png")
        cv2.imwrite(output_path, cropped_image)
        print("Cropped image saved to:", output_path)
        return True
    except Exception as e:
        print("Error in screenshot_math:", e)
        return False
