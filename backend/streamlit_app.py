
import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"

def get_documents():
    try:
        res = requests.get(f"{API_URL}/documents")
        data = res.json()

        if isinstance(data, dict):
            return data.get("documents", [])
        return data

    except:
        return []



# page configurations

st.set_page_config(
    page_title="GenAI Document Assistant",
    layout="wide"
)



# custom css

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1020;
        color: white;
    }

    h1, h2, h3 {
        color: white;
    }

    .main-title {
        font-size: 52px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 34px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .answer-box {
        background-color: #111827;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #374151;
        margin-top: 15px;
        color: white;
        font-size: 18px;
    }

    .sidebar-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .uploaded-box {
        background-color: #1f2937;
        padding: 12px;
        border-radius: 12px;
        margin-top: 10px;
        color: white;
    }

    .success-box {
        background-color: #14532d;
        padding: 14px;
        border-radius: 12px;
        color: #bbf7d0;
        font-weight: 500;
        margin-top: 15px;
    }

    div.stButton > button {
        background-color: #111827;
        color: white;
        border-radius: 10px;
        border: 1px solid #374151;
        padding: 10px 24px;
        font-size: 18px;
        font-weight: 500;
    }

    div.stButton > button:hover {
        background-color: #1f2937;
        border: 1px solid #6b7280;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# session state

if "docs_uploaded" not in st.session_state:
    st.session_state.docs_uploaded = False



# sidebar

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">📂 Upload Knowledge Base</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload PDF file",
        type=["pdf"]
    )

    if uploaded_file is not None:

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            response = requests.post(
                f"{API_URL}/upload",
                files=files
            )

            if response.status_code == 200:

                st.session_state.docs_uploaded = True

                st.markdown(
                    f'''
                    <div class="uploaded-box">
                        📄 {uploaded_file.name}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '''
                    <div class="success-box">
                        ✅ Document loaded successfully!
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            else:
                st.error("Upload failed")

        except Exception as e:
            st.error(f"Error: {str(e)}")



    st.markdown("---")
    st.markdown("### 📁 Manage Documents")

    if st.button("📄 Show Uploaded Documents"):
        
        st.write(requests.get(f"{API_URL}/documents").json())  # 👈 DEBUG LINE

        documents = get_documents()

        if not documents:
            st.info("No documents uploaded yet.")
        else:
            for doc in documents:

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"📄 {doc['filename']}")

                with col2:
                    if st.button("🗑️", key=f"del_{doc['id']}"):

                        try:
                            res = requests.delete(
                                f"{API_URL}/documents/{doc['id']}"
                            )

                            if res.status_code == 200:
                                st.success("Deleted")
                                st.rerun()
                            else:
                                st.error("Delete failed")

                        except Exception as e:
                            st.error(str(e))


# main content

st.markdown(
    '<div class="main-title">📚 GenAI Document Assistant System</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">💬 Ask a Question</div>',
    unsafe_allow_html=True
)


query = st.text_input(
    "Type your question here",
    placeholder="Ask anything about the uploaded document..."
)


if st.button("Get Answer"):

    if not st.session_state.docs_uploaded:
        st.warning("⚠️ Please upload a PDF first.")
        st.stop()

    if not query.strip():
        st.warning("⚠️ Enter a valid question.")
        st.stop()

    try:

        response = requests.post(
            f"{API_URL}/ask",
            json={"query": query}
        )

        data = response.json()

        st.markdown(
            '<div class="section-title">🧠 Answer</div>',
            unsafe_allow_html=True
        )

        if response.status_code == 200:

            if "answer" in data:

                st.markdown(
                    f'''
                    <div class="answer-box">
                        {data["answer"]}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            elif "response" in data:

                st.markdown(
                    f'''
                    <div class="answer-box">
                        {data["response"]}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            else:
                st.error("No answer returned from API")
                st.write(data)

        else:
            st.error(f"API Error: {data}")

    except Exception as e:
        st.error(f"Error generating answer: {str(e)}")

