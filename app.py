import streamlit as st

# --- Page Setup ---
chat_page = st.Page(
    page="views/chat.py",
    title="Chat",
    icon=":material/chat:",
    default=True
)

upload_docs_page = st.Page(
    page="views/upload_docs.py",
    title="Upload Document",
    icon=":material/upload_file:",
)

chat_spesific_page = st.Page(
    page="views/chat_spesific_docs.py",
    title="Chat Spesific Docs",
    icon=":material/chat:",
)

# --- Navigation Setup ---
pg = st.navigation(
    {
        "Chat Bot PPKS" : [chat_page, upload_docs_page, chat_spesific_page]
    },
)


# --- Navigation Run ---
pg.run()
        