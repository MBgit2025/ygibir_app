#frontend/app.py


##Step 1: Create the Streamlit Frontend File
##Create a folder named frontend in your main project directory (C:\zGitDok\GibirApp).
##Inside the frontend folder, create a new Python file named app.py.
##Step 2: Write the Basic Streamlit Code (frontend/app.py)
##This initial code will do three things:
##Display a title.
##Have a button.
##When the button is pressed, it will make a request to your running FastAPI server.
##In your frontend/app.py, add the following:





import streamlit as st
import requests
from FAPI_Fourth import read_hello, calculate_tax, handle_calculation, DB_NAME

# The base URL of your running FastAPI backend
# Note: FastAPI is running on http://127.0.0.1:8000
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("My Streamlit Frontend")
st.markdown("---")

# --- Example 1: Check the API status (if you have a root route `/`) ---
# If your API only has routes like `/items`, replace the endpoint below

# If you want to test a specific API endpoint, you'll need to define one in FAPI_Fourth.py first.
# Let's assume you've added a simple test route in FAPI_Fourth.py:
#
# @app.get("/hello")
# def read_root():
#     return {"message": "Hello from FastAPI!"}
#

# We will try to call a placeholder endpoint: `/hello`
ENDPOINT = "/hello"

if st.button("Click to Call FastAPI"):
    try:
        # Make the GET request to the FastAPI server
        response = requests.get(f"{FASTAPI_URL}{ENDPOINT}")
        
        if response.status_code == 200:
            data = response.json()
            st.success("Successfully connected to FastAPI!")
            st.json(data) # Display the JSON response
        elif response.status_code == 404:
            st.error(f"Error: 404 Not Found. Make sure the route '{ENDPOINT}' is defined in your FastAPI app (FAPI_Fourth.py).")
        else:
            st.error(f"Error connecting to FastAPI. Status code: {response.status_code}")
            st.write(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error(
            "Connection Error! Is your FastAPI server running? "
            f"It should be running in a separate terminal at: {FASTAPI_URL}"
        )
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

##Step 3: Add a Test Endpoint to FastAPI (Crucial)
##To make the Streamlit app work, you need an endpoint for it to call.
##In your FAPI_Fourth.py file, add this simple test route (make sure to import FastAPI if you haven't already):
##code
##Python

# FAPI_Fourth.py
##from fastapi import FastAPI

##app = FastAPI()
##
### Add this new route
##@app.get("/hello")
##def read_hello():
##    return {"message": "Hello from FastAPI!", "status": "Backend is operational"}

# ... your other routes will go here
##Step 4: Run the Streamlit Frontend
##Verify FastAPI is running: Check your first terminal—it should still show the Uvicorn log: INFO: Uvicorn running on http://127.0.0.1:8000.
##Open a second terminal/tab.
##Navigate to your project root: C:\zGitDok\GibirApp
##Run the Streamlit app:
##code
##Bash
##(dict_app) C:\zGitDok\GibirApp>streamlit run frontend/app.py
##Streamlit will open a browser window for you (usually at http://localhost:8501).
##Now, when you click the button in the Streamlit app, it will make a network request to your FastAPI server, and you should see
##the {"message": "Hello from FastAPI!", ...} response displayed!
