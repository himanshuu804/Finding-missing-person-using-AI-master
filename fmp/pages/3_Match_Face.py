import json
import os
import streamlit as st
from pages.helper import db_queries
from pages.helper.utils import image_obj_to_numpy, extract_face_mesh_landmarks, compare_face_meshes
from pages.helper.streamlit_helpers import require_login

st.set_page_config(page_title="Match Face")
require_login()

st.title("🤖 AI Face Matching")
st.write("Upload a photo to match against all registered missing persons.")

image_obj = st.file_uploader("Upload Photo to Match", type=["jpg", "jpeg", "png"])

threshold = st.slider("Similarity Threshold", min_value=0.1, max_value=1.0, value=0.6, step=0.05,
                      help="Higher = stricter match. 0.6 is recommended.")

if image_obj:
    st.image(image_obj, caption="Query Image", width=200)

    with st.spinner("Extracting face data..."):
        image_numpy = image_obj_to_numpy(image_obj)
        query_mesh = extract_face_mesh_landmarks(image_numpy)

    if not query_mesh:
        st.error("❌ No face detected in the uploaded image. Please try a clearer frontal photo.")
    else:
        st.success("✅ Face detected. Searching database...")

        cases = db_queries.get_all_missing_cases()
        matches = []

        for case in cases:
            if not case.face_mesh:
                continue
            score = compare_face_meshes(json.dumps(query_mesh), case.face_mesh)
            if score >= threshold:
                matches.append((score, case))

        matches.sort(key=lambda x: x[0], reverse=True)

        if matches:
            st.success(f"🎯 Found **{len(matches)}** potential match(es)!")
            for score, case in matches:
                with st.expander(f"Match: {case.name} — Similarity: {score*100:.1f}%"):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if case.image_path and os.path.exists(case.image_path):
                            st.image(case.image_path, width=160)
                    with col2:
                        st.write(f"**Name:** {case.name}")
                        st.write(f"**Age:** {case.age or 'N/A'}")
                        st.write(f"**Last Seen:** {case.location_last_seen or 'N/A'}")
                        st.write(f"**Birth Marks:** {case.birth_marks or 'N/A'}")
                        st.write(f"**Contact:** {case.contact_number or 'N/A'}")
                        st.progress(score)
        else:
            st.warning("No matches found above the threshold. Try lowering the threshold or use a clearer image.")

        # Also check public submissions
        st.write("---")
        st.subheader("📱 Public Submissions Match")
        submissions = db_queries.get_all_public_submissions()
        sub_matches = []

        for sub in submissions:
            if not sub.face_mesh:
                continue
            score = compare_face_meshes(json.dumps(query_mesh), sub.face_mesh)
            if score >= threshold:
                sub_matches.append((score, sub))

        sub_matches.sort(key=lambda x: x[0], reverse=True)

        if sub_matches:
            st.success(f"Found **{len(sub_matches)}** match(es) in public submissions!")
            for score, sub in sub_matches:
                with st.expander(f"Public Submission by {sub.submitted_by} — {score*100:.1f}%"):
                    st.write(f"**Submitted By:** {sub.submitted_by}")
                    st.write(f"**Location:** {sub.location}")
                    st.write(f"**Mobile:** {sub.mobile}")
                    st.write(f"**Email:** {sub.email}")
                    st.progress(score)
        else:
            st.info("No matches in public submissions.")
