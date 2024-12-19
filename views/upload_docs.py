import streamlit as st
import tempfile
import pathlib
import asyncio
import re
import time
import math
import os
from collections import Counter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_parse import LlamaParse
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase
from langchain_community.graphs import Neo4jGraph
from langchain_groq import ChatGroq
from rapidfuzz import fuzz, process
from langchain_core.documents import Document

st.set_page_config(
    page_title="PPKS | Upload Document",
    page_icon="assets/ELA 1x1.jpg",
    layout="wide",
)

# os.environ["NEO4J_URI"] = st.secrets['neo4j_upload_docs']['NEO4J_URI']
# os.environ["NEO4J_USERNAME"] = st.secrets['neo4j_upload_docs']['NEO4J_USERNAME']
# os.environ["NEO4J_PASSWORD"] = st.secrets['neo4j_upload_docs']['NEO4J_PASSWORD']


if "llm" not in st.session_state:
    st.session_state.llm = []

if 'convert_disabled' not in st.session_state:
    st.session_state.convert_disabled = True

if 'convert_status' not in st.session_state:
    st.session_state.convert_status = None

if 'uploaded_doc' not in st.session_state:
    st.session_state.uploaded_doc = None

if 'conversion_done' not in st.session_state:
    st.session_state.conversion_done = None

if 'conversion_running' not in st.session_state:
    st.session_state.conversion_running = None

load_dotenv()

# Load llm model using Groq
@st.cache_resource
def load_llm_groq(API_KEY):
    return ChatGroq(
        model='llama-3.1-70b-versatile',
        api_key=API_KEY
    )

st.session_state.llm = [
    load_llm_groq(st.secrets['groq_key_for_convert']['groq_1']),
    load_llm_groq(st.secrets['groq_key_for_convert']['groq_2']),
    load_llm_groq(st.secrets['groq_key_for_convert']['groq_3']),
]


@st.cache_resource
def load_knowledge_graph():
    return Neo4jGraph(
        url = st.secrets['neo4j_upload_docs']["NEO4J_URI"],
        username = st.secrets['neo4j_upload_docs']["NEO4J_USERNAME"],
        password = st.secrets['neo4j_upload_docs']["NEO4J_PASSWORD"],
    )

graph = load_knowledge_graph()

def find_duplicate_header(text, headers, ratio=fuzz.QRatio, Thres=90):
    result = process.extractOne(text, headers, scorer=ratio)
    if result is not None:
        if result[1] >=Thres:
            return True
    return False

async def parsing_document(file_path):
    print("CONVERT_STATUS:\tPARSING DOCUMENT")
    
    # set up parser
    parser = LlamaParse(
        result_type="markdown",
        page_separator="\n---\n",
        is_formatting_instruction=False,
    )

    return await parser.aget_json(file_path)

def preprocessing_documents(json_file, metadata):
    # Extract total pages
    metadata['total_pages'] = json_file['job_metadata']['job_pages']

    # List to store every header
    headers = []

    # langchain document list
    list_doc = []

    # Heading flag
    have_heading = False

    for page in json_file['pages']:
        
        # temp
        _document_str = []

        # extract metadata for every pages
        metadata['page'] = page['page']

        # extracting all the content
        for item in page['items']:

            # Finding if content type is Heading
            if item['type'] == 'heading':

                # Cheking if heading already have or no
                if not find_duplicate_header(item['md'].lower(), headers, fuzz.QRatio, 90):

                    # We need flag here
                    if have_heading and len(_document_str) != 0:
                        # create langchain document
                        list_doc.append(
                            Document(
                                metadata=metadata,
                                page_content = "\n\n".join(_document_str)
                            )
                        )

                        # free the document temp
                        _document_str = []

                    _document_str.append(item['md'])
                    headers.append(item['md'].lower())

                    # switch the flag
                    have_heading = True
            else :
                _document_str.append(item['md'])

        # create langchain document
        list_doc.append(
            Document(
                metadata=metadata,
                page_content = "\n\n".join(_document_str)
            )
        )

    return list_doc   

def create_chunks(documents):
    return_chunks = []

    chunk_size =1816
    chunk_overlap = 64
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Split
    chunks = text_splitter.split_documents(documents)

    chunks_len = len(chunks)
    
    if chunks_len < 12:
        step = 1
        for i in range(0, chunks_len, step):
            return_chunks.append(chunks[i:i+step])
    else:
        step = math.ceil(chunks_len/12)

        for i in range(0, chunks_len, step):
            return_chunks.append(chunks[i:i+step])
    
    return return_chunks  

async def convert_and_add_graph_from_doc(llm, graph, chunks):

    # load llm tranformer
    llm_transformer = LLMGraphTransformer(llm=llm)

    #convert graph
    print("CONVERT_STATUS:\tCONVERT CHUNKS TO GRAPH")
    graph_documents = await llm_transformer.aconvert_to_graph_documents(chunks)

    print("CONVERT_STATUS:\tADDING GRAPH TO NEO4J")
    graph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
        include_source=True
    )

async def convert_document(file_path, llms, graph, metadata):
    
    with st.status("Converting Document...", expanded=True) as status:
        try:
            # Load and Clean Document
            st.write("Parsing Document...")
            parsing_result = await parsing_document(file_path)

            st.write("Cleaning Document...")
            documents = preprocessing_documents(parsing_result[0], metadata)

            # Chunking Document
            st.write("Chunking Document...")
            chunks = create_chunks(documents)

            progress_text = "Add Document Graph..."
            my_bar = st.progress(0, text=progress_text)

            chunks_len = len(chunks)
            if len(chunks) < 12:
                progress_increment = 100/chunks_len
                progress = 0
                
                for idx in range(chunks_len):
                    llm_list_idx = [0,1,2,0,1,2,0,1,2,0,1,2]
                    llm_idx = llm_list_idx[idx]

                    task = asyncio.create_task(convert_and_add_graph_from_doc(llm=llms[llm_idx], graph=graph, chunks=chunks[idx]))
                    await asyncio.sleep(10)
                    await task
                    
                    progress += progress_increment

                    my_bar.progress(progress/100, text=progress_text)
                    
                    
            else :
                progress_increment = 100/chunks_len
                progress = 0

                for idx in range(len(chunks)):
                    llm_list_idx = [0,1,2,0,1,2,0,1,2,0,1,2]
                    llm_idx = llm_list_idx[idx]

                    task = asyncio.create_task(convert_and_add_graph_from_doc(llm=llms[llm_idx], graph=graph, chunks=chunks[idx]))
                    await asyncio.sleep(20)
                    await task
                    
                    progress += progress_increment

                    my_bar.progress(progress/100, text=progress_text)

            my_bar.empty()

            status.update(
                label="Converting Completed!", state="complete", expanded=False
            )

            st.session_state.conversion_running = False
            st.session_state.conversion_done = True
        except Exception as e:
            status.update(
                label="Converting Failed!", state="error", expanded=False
            )

            st.write(e)

# def delete_knoledge_graph_db():
#====================================================================================================#

def on_change_file_uploader():
    st.session_state.convert_disabled = not st.session_state.convert_disabled

def on_click_convert_button():
    st.session_state.convert_disabled = not st.session_state.convert_disabled

with st.container():
    st.header("Sumber Pengetahuan Chat Bot", divider="grey")
    st.write(
        """
        Silahkan *upload document* yang akan menjadi sumber pengetahuan yang ingin ada *explore* menggunakan Chat Bot!
        """
    )

col_upload = st.columns([0.4, 0.6])

with st.container():
    with col_upload[0]:
        with st.container(height=360, border=True):
            st.write(
                """
                #### Convert Settings
                """)

            option_map = {
                0: "Accurate",
                1: "Fast (soon)",
            }

            selection = st.segmented_control(
                "**MODE**",
                disabled=True,
                options=option_map.keys(),
                format_func=lambda option: option_map[option],
                selection_mode="single",
                default=0,
                help="1. Accurate Mode : using LlamaParse to extract PDF document.(Takes more time, but extraction result is awesome).\n2. Fast Mode : using PyMuPDF library to extract PDF document. (Very Fast but extraction result is depend on doc layout)."
            )

        
    with col_upload[1]:
        with st.container(border=True):

            temp_dir = tempfile.TemporaryDirectory()
            
            uploaded_doc = st.file_uploader(
                label="Upload Document",
                type=['pdf', 'docx', 'txt'],
                accept_multiple_files=False,
                label_visibility="visible",
                on_change=on_change_file_uploader
                )


            if uploaded_doc is not None:
                st.session_state.convert_disabled = False
                uploaded_doc_name = uploaded_doc.name
                uploaded_doc_path = pathlib.Path(temp_dir.name) / uploaded_doc_name
                
                meta_file_name = {
                    'source' : uploaded_doc_name
                }

                with open(uploaded_doc_path, 'wb') as output_temporary_file:
                    output_temporary_file.write(uploaded_doc.read())


        
            if st.button(label="Convert", type="primary", disabled=st.session_state.convert_disabled, use_container_width=True, on_click=on_click_convert_button):
                asyncio.run(convert_document(file_path=uploaded_doc_path, llms=st.session_state.llm, graph=graph, metadata=meta_file_name))
                
