import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
import json

def generate_krl_code(points, motion_type="LIN", start_point="HOME"):
    """
    Generates KRL code from a list of points.
    """
    krl_code = "DEF Path_Program()\n"
    krl_code += "; Initialization\n"
    krl_code += "BAS (#INITMOV,0)\n"
    
    if start_point == "HOME":
        krl_code += "PTP HOME\n\n"
    
    krl_code += "; Path execution\n"

    if motion_type == "SPLINE (simplified)":
        krl_code += "SPLINE\n"
        for point in points:
            x = point[0]
            y = point[1]
            krl_code += f"  SLIN {{X {x}, Y {y}, Z 0, A 0, B 0, C 0}}\n"
        krl_code += "ENDSPLINE\n"
    else:
        for point in points:
            x = point[0]
            y = point[1]
            if motion_type == "LIN":
                krl_code += f"LIN {{X {x}, Y {y}, Z 0, A 0, B 0, C 0}}\n"
            elif motion_type == "PTP":
                krl_code += f"PTP {{X {x}, Y {y}, Z 0, A 0, B 0, C 0}}\n"

    if start_point == "HOME":
        krl_code += "\nPTP HOME\n"
        
    krl_code += "END\n"
    
    return krl_code

def process_image(image_bytes):
    """
    Processes the uploaded image to find contours.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return [], None

    largest_contour = max(contours, key=cv2.contourArea)
    points = largest_contour.reshape(-1, 2).tolist()
    
    cv2.drawContours(img, [largest_contour], -1, (0, 255, 0), 3)
    
    return points, img

st.set_page_config(layout="wide")
st.title("Sketch-to-KRL Code Generator")

# --- Sidebar for options ---
st.sidebar.header("KRL Generation Options")
motion_type = st.sidebar.selectbox("Motion Type", ["LIN", "PTP", "SPLINE (simplified)"])
start_point = st.sidebar.radio("Start Point", ["HOME", "Current Position"])
store_sketch = st.sidebar.checkbox("Store sketch and code")

# --- Main content ---
input_method = st.radio("Choose your input method:", ("Upload an image", "Draw a sketch"))

points = []
processed_image = None

if input_method == "Upload an image":
    uploaded_file = st.file_uploader("Upload a sketch", type=["jpg", "png"])
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        st.image(image_bytes, caption="Uploaded Sketch", width=400)
        if st.button("Process Image"):
            points, processed_image = process_image(image_bytes)

elif input_method == "Draw a sketch":
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=5,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        if canvas_result.json_data["objects"]:
            # This is a simplified way to get points from the drawing.
            # It takes the path from the first object drawn.
            path = canvas_result.json_data["objects"][0]["path"]
            points = [p[1:3] for p in path]


if points:
    st.subheader("Detected Path Points")
    st.write(f"{len(points)} points detected.")

    if processed_image is not None:
        st.subheader("Processed Image")
        st.image(processed_image, caption="Processed Image with Detected Path", width=400)

    st.subheader("Generated KRL Code")
    krl_code = generate_krl_code(points, motion_type, start_point)
    st.code(krl_code, language="krl")

    st.download_button(
        label="Download .src file",
        data=krl_code,
        file_name="path_program.src",
        mime="text/plain",
    )

    st.subheader("JSON Representation of Path")
    json_output = json.dumps({"path_points": points}, indent=4)
    st.code(json_output, language="json")
    
    st.download_button(
        label="Download path.json",
        data=json_output,
        file_name="path.json",
        mime="application/json",
    )

if store_sketch:
    st.sidebar.info("Note: Storing sketch and code is not yet implemented.")
