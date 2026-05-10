import streamlit as st
from pages.helper import db_queries
from pages.helper.streamlit_helpers import require_login

st.set_page_config(page_title="Public Submissions")
require_login()

st.title("📱 Public Submissions")
st.write("Sightings and tips submitted by the public via the mobile app.")

submissions = db_queries.get_all_public_submissions()

if not submissions:
    st.info("No public submissions yet.")
else:
    st.write(f"**Total Submissions: {len(submissions)}**")
    for sub in submissions:
        with st.expander(f"Submission by {sub.submitted_by or 'Anonymous'} — {sub.location or 'Unknown location'}"):
            st.write(f"**Name:** {sub.submitted_by or 'N/A'}")
            st.write(f"**Location:** {sub.location or 'N/A'}")
            st.write(f"**Mobile:** {sub.mobile or 'N/A'}")
            st.write(f"**Email:** {sub.email or 'N/A'}")
            st.write(f"**Birth Marks:** {sub.birth_marks or 'N/A'}")
            face_detected = sub.face_mesh and sub.face_mesh != "[]"
            st.write(f"**Face Data:** {'✅ Captured' if face_detected else '❌ Not captured'}")
