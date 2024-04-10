import os
import requests
import uuid

UPLOAD_URL = 'http://localhost:25000/upload'
PROCESS_URL = 'http://localhost:25000/process'


def upload_and_process_file(file_path):
    try:
        # Upload the file
        files = {'file': open(file_path, 'rb')}
        upload_response = requests.post(UPLOAD_URL, files=files)
        if upload_response.status_code == 200:
            user_id = upload_response.json().get("user_id")
            print("File uploaded successfully with user ID:", user_id)
            
            # Process the uploaded file
            process_response = process_file(user_id)
            if process_response.status_code == 200:
                print("File processed successfully.")
                response_json = process_response.json()
                if 'mock_exam' in response_json:
                    print(response_json['mock_exam'])  # Print the message from the JSON response
                else:
                    print("Unexpected response format.")
            else:
                print("Error processing the file:", process_response.json().get('error'))
        else:
            print("Error uploading the file:", upload_response.json().get('error'))
    except Exception as e:
        print("Error:", e)


def process_file(user_id):
    try:
        # Send user ID to request processing
        cookies = {'user_id': user_id}
        response = requests.post(PROCESS_URL, cookies=cookies)
        
        return response
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    file_path = './Resources/Test_4_Pages.pdf'  # Replace with the path to the uploaded PDF file
    upload_and_process_file(file_path)
