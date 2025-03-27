A brief description of what this project does and its purpose.

## Installation

### Prerequisites

- Python 3.8+
- Git (for cloning the repository)
- Virtual Environment (recommended)

## Cloning the Repository

Open your terminal or command prompt.
Run the following command to clone the repository:

git clone https://github.com/Varshith3/Python_Backend_LLM_Summarization.git

## Running the Project

### Install the required dependencies using pip:

pip install -r requirements.txt

### Set Up Environment Variables
Make sure to create a .env file in the root of the project.

API_KEY=your-api-key

After installing the dependencies and setting up the environment, you can run the project.

### To run the FastAPI server locally, execute:

uvicorn main:app --reload
This will start the server at http://127.0.0.1:8000

### For frontend run the following command:

streamlit run app.py

This will start the Streamlit app locally, typically at http://localhost:8501.
