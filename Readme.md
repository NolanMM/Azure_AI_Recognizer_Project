## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

_The Instruction for installing and set up the project locally._

### Quick Installation
  
### Create Virtual Environment and Install Dependencies

1.1. Before running the code examples, make sure you have the virtual enviroment is installed and be ready to use:
We need to create a new `Python 3.11` / `Python 3.10` virtual enviroment for this project.

* If you want to create a new virtual enviroment, you can use the following command in the terminal of the project directory:

  * In Windows or Linux, you can use the following command:
  
  ```bash
    python -m venv venv
  ```

  * Then, you can activate the virtual enviroment by using the following command:
  
  ```bash
    venv\Scripts\activate
  ```

  * In MacOs, you can use the following command:
  
  ```bash
    python3 -m venv venv
  ```

  * Then, you can activate the virtual enviroment by using the following command:
  
  ```bash
    source venv/Scripts/activate
  ```

* Make sure the virtual environment needed for project is activate with corresponding project directory, you can use the following command:

  * In Windows or Linux, you can use the following command:
  
  ```bash
    venv\Scripts\activate
  ```

  * In MacOs, you can use the following command:
  
  ```bash
    source venv/Scripts/activate
  ```

* Option 1: Install dependencies using pip package:
  
  ```bash
    pip install AI-ML-Formulas-Recognizer-Extraction==1.0
  ```
  
* Option 2: Install requirements.txt: Automatically installed dependencies that needed for the project:
  
  ```bash
    pip install -r requirements.txt
  ```

</br>

### Usage

To use the code examples in this repository, follow these steps:

1. Install the required dependencies as mentioned in the [Prerequisites](#prerequisites) section.

2. Modify the key (Replace "ImportKEY" by your key) for OpenAI Services in Azure_AI_RECOGNIZER/Services/Images_Services/openai_module.py

3. Run the following command in the terminal to start the server:

* Run the server:
  
  ```bash
    python main.py
  ```
  
* Run the client:
  
  ```bash
    python client.py
  ```

</br>
