from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import uuid
from Services.Directory_Control_Services.DirectoryControl import delete_folder
from Services.Pdf_Services.DefineTextInPdfPage import process_page
from Services.Images_Services.openai_module import OpenAI_Module
import time
import os
import tqdm
import multiprocessing
import threading
import pdfplumber

# Dictionary to store user IDs and their corresponding file paths
user_files = {}

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


num_cores = multiprocessing.cpu_count()
max_threads = num_cores * 2 - 2


def main_process(file_path, user_id):
    start_time = time.time()  # Record start time
    # Load the PDF file and convert each page to an image
    pdf_file_path = file_path
    results = {}
    # Decrease this number if your system can't run the code as it is resource-intensive
    batches = 6

    # Create a folder to store the output images
    user_folder = os.path.join(os.getcwd(), "output_images", user_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    with pdfplumber.open(pdf_file_path) as pdf:
        # Use tqdm for progress tracking
        for i in tqdm.tqdm(range(0, len(pdf.pages), batches), desc="Processing Batches"):
            threads = []
            for j in range(i, min(i + batches, len(pdf.pages))):
                page_number = j + 1
                # Save each page as an image
                page = pdf.pages[j]
                image_path = os.path.join(user_folder, f"page_{page_number}.png")
                page.to_image().save(image_path)

                # Define all the text in the image
                thread = threading.Thread(target=process_page, args=(image_path, page_number, user_folder, results))
                threads.append(thread)
                thread.start()

                # Limit the number of active threads (wait for any threads to finish before starting new ones)
                active_threads = threading.active_count()
                while active_threads >= max_threads:
                    # Wait for a short duration before checking again
                    threading.Event().wait(0.2)
                    active_threads = threading.active_count()

            # Wait for all threads in this batch to finish
            for thread in threads:
                thread.join()

    # Sort the results dictionary by page number
    sorted_results = {key: value for key, value in sorted(results.items(), key=lambda item: item[0])}
    #print(sorted_results)

    Final_Exam = OpenAI_Module(sorted_results)

    total_time = time.time() - start_time  # Calculate total time
    print(f"\nTotal time taken: {total_time} seconds")
    return Final_Exam


def upload_file(file, user_id):
    if file and file.filename.endswith(".pdf"):
        user_folder = os.path.join("./output_images", user_id)  # Create a folder for the user
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        file_path = os.path.join(user_folder, file.filename)  # Save the file in the user's folder
        file.save(file_path)
        user_files[user_id] = file_path  # Store the user ID and file path
        response_data = {
            "message": "File uploaded successfully",
            "user_id": user_id
        }
        return response_data
    else:
        return "Invalid file format, only PDF files are allowed"


def process_file(user_id):
    try:
        file_path = user_files.get(user_id)
        if not file_path or not os.path.exists(file_path):
            return jsonify({"error": "File not found or associated with the user"}), 404

        results = main_process(file_path, user_id)
        folder_to_delete = os.path.join('output_images', user_id)
        delete_folder(folder_to_delete)
        # Remove the user ID and file path from the dictionary after processing delete the folder
        user_files.pop(user_id, None)
        return results
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message as a dictionary with status code 500


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    user_id = str(uuid.uuid4())  # Generate a unique ID for the user
    response = upload_file(file, user_id)
    if isinstance(response, dict):
        response = make_response(jsonify(response), 200)
        response.set_cookie("user_id", user_id)
        return response
    else:
        return jsonify({"error": response}), 400


@app.route("/process", methods=["POST"])
def process():
    user_id = request.cookies.get('user_id')
    if not user_id:
        return jsonify({"error": "No user ID provided"}), 400

    response_data = process_file(user_id)

    if not isinstance(response_data, Exception):
        response = jsonify(response_data)
        final_response = make_response(response)
        final_response.delete_cookie("user_id")
        final_response.status_code = 200
        return final_response
    else:
        error_message = str(response_data)
        return jsonify({"error": error_message}), 500
    

def main():
    if not os.path.exists("./uploads"):
        os.makedirs("./uploads")
    app.run(debug=True, port=25000)


if __name__ == "__main__":
    main()
