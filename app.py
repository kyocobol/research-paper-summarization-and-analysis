import logging
import os

import streamlit as st

from config import DATA_DIR
from workflow.graph import build_workflow

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

st.title("Automated Research Paper Summarization and Analysis")
workflow = build_workflow()

uploaded_file = st.file_uploader(
    "Upload a PDF file of the research paper.", type=["pdf"]
)

if uploaded_file:
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Generating report..."):
        try:
            logger.info("Workflow started")
            state = workflow.invoke({"file_path": file_path})
            logger.info("Workflow completed")
        except Exception:
            logger.exception("Workflow failed")
            st.error("An error occurred during report generation.")
            raise

    st.subheader("Report")
    st.markdown(state["final_report"])
