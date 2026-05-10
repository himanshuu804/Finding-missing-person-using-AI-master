import uuid
import json
import streamlit as st
from pages.helper import db_queries
from pages.helper.data_models import MissingPerson
from pages.helper.utils import image_obj_to_numpy, extract_face_mesh_landmarks
from pages.helper.streamlit_helpers import require_login

st.set_page_config(page_title="Register Case")
require_login()

st.title("📋 Register New Missing Person Case")

with st.form(key="register_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name *")
        age = st.number_input("Age", min_value=0, max_value=120, value=0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact_number = st.text_input("Contact Number")

    with col2:
        location_last_seen = st.text_input("Location Last Seen")
        birth_marks = st.text_input("Birth Marks / Identifiers")
        description = st.text_area("Additional Description")

    image_obj = st.file_uploader("Upload Photo *", type=["jpg", "jpeg", "png"])

    submit = st.form_submit_button("Register Case")

if submit:
    if not name:
        st.error("Name is required.")
    elif not image_obj:
        st.error("Please upload a photo.")
    else:
        with st.spinner("Processing image and extracting face data..."):
            unique_id = str(uuid.uuid4())
            image_path = f"./resources/{unique_id}.jpg"

            image_obj.seek(0)
            with open(image_path, "wb") as f:
                f.write(image_obj.read())

            image_numpy = image_obj_to_numpy(image_obj)
            face_mesh = extract_face_mesh_landmarks(image_numpy)

            person = MissingPerson(
                id=unique_id,
                name=name,
                age=age if age > 0 else None,
                gender=gender,
                location_last_seen=location_last_seen,
                birth_marks=birth_marks,
                description=description,
                contact_number=contact_number,
                face_mesh=json.dumps(face_mesh),
                registered_by=st.session_state.get("user", "Unknown"),
                image_path=image_path,
                status="NF",
            )

            db_queries.new_missing_case(person)

        st.success(f"✅ Case registered successfully! ID: `{unique_id}`")
        if not face_mesh:
            st.warning("⚠️ No face detected in the image. Matching may not work. Try a clearer frontal photo.")
