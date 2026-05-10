import base64
import streamlit as st
import pandas as pd
from pages.helper import db_queries
from pages.helper.streamlit_helpers import require_login

st.set_page_config(page_title="View Cases")
require_login()

st.title("🔍 All Missing Person Cases")

cases = db_queries.get_all_missing_cases()

if not cases:
    st.info("No cases registered yet.")
else:
    status_filter = st.selectbox("Filter by Status", ["All", "Not Found (NF)", "Found (F)"])

    filtered = cases
    if status_filter == "Not Found (NF)":
        filtered = [c for c in cases if c.status == "NF"]
    elif status_filter == "Found (F)":
        filtered = [c for c in cases if c.status == "F"]

    st.write(f"**{len(filtered)} case(s) found**")

    for case in filtered:
        with st.expander(f"{'🔴' if case.status == 'NF' else '🟢'} {case.name} — ID: {case.id[:8]}..."):
            col1, col2 = st.columns([1, 2])

            with col1:
                if case.image_path:
                    try:
                        image_bytes = base64.b64decode(case.image_path)
                        st.image(image_bytes, width=180)
                    except:
                        st.write("📷 No image")
                else:
                    st.write("📷 No image")

            with col2:
                st.write(f"**Name:** {case.name}")
                st.write(f"**Age:** {case.age or 'N/A'}")
                st.write(f"**Gender:** {case.gender or 'N/A'}")
                st.write(f"**Last Seen:** {case.location_last_seen or 'N/A'}")
                st.write(f"**Birth Marks:** {case.birth_marks or 'N/A'}")
                st.write(f"**Contact:** {case.contact_number or 'N/A'}")
                st.write(f"**Registered By:** {case.registered_by or 'N/A'}")
                st.write(f"**Status:** {'🔴 Not Found' if case.status == 'NF' else '🟢 Found'}")

                new_status = "F" if case.status == "NF" else "NF"
                label = "✅ Mark as Found" if case.status == "NF" else "🔄 Mark as Not Found"
                if st.button(label, key=f"status_{case.id}"):
                    db_queries.update_missing_person_status(case.id, new_status)
                    st.success("Status updated!")
                    st.rerun()

                if st.button("🗑️ Delete Case", key=f"del_{case.id}"):
                    db_queries.delete_missing_person(case.id)
                    st.warning("Case deleted.")
                    st.rerun()
