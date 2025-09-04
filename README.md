# Sketch-to-KRL Code Generator

This is a Streamlit web application that converts a sketch of a robot path into KUKA KRL code.

## How to run locally

1.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## How to deploy to HuggingFace Spaces

1.  Create a new Space on HuggingFace: [https://huggingface.co/new-space](https://huggingface.co/new-space)
2.  Choose "Streamlit" as the SDK.
3.  Choose a name for your Space.
4.  Create a new `app.py` file in the Space and paste the code from this project'''s `app.py`.
5.  Create a new `requirements.txt` file in the Space and paste the content from this project'''s `requirements.txt`.
6.  The Space will build and deploy automatically. You will get a public URL for your application.
