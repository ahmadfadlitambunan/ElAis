#

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h1 align="center">ElAis</h1>

  <p align="center">
    An awesome chat AI to get know what you want to ask about PPKS profile, products and services!
    <br />
    <a href="https://chatbot-ppks.streamlit.app/"><strong>View demo »</strong></a>
    <br />
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#feature">Feature</a></li>
    <li><a href="#arcitecture">Arcitecture</a></li>
    <li><a href="#reference">References</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

<p align="center">
  <img src="image\ELA 1x1.jpg" alt="Image" width="320" height="320">
</p>

ElAis adalah asisten tanya jawab inovatif yang menggunakan teknologi Artificial Intelligence untuk memberikan interaksi cerdas dan relevan mengenai profile, layanan jasa, serta produk dan riset yang dikembangkan oleh Pusat Penelitian Kelapa Sawit (PPKS). Menggunakan Generative AI (LLM), aplikasi ini dapat memberikan jawaban yang akurat dan cepat sesuai dengan pertanyaan pengguna, serta memahami konteks percakapan dengan baik.

Dari sisi bisnis, produk ini memberikan solusi yang tepat untuk memperkuat dukungan pelanggan, meningkatkan proses internal, dan memberikan pengalaman pengguna yang lebih baik dengan biaya yang lebih rendah dibandingkan metode tradisional seperti fine-tuning model besar.

<p align="right"><a href="#">🔝</a></p>

<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repository

   ```sh
   git clone https://github.com/ahmadfadlitambunan/ElAis.git
   ```
2. Set env variable

   
    
3. Create virtual environment
   
   ```sh
    python -m venv nama-virtual-env # if using python
  
    conda create -m nama-virtual-env python=3.10 # if using conda
   ```

   Then activate it.

    ```sh
    nama-virtual-env\Scripts\activate # if using python

    conda activate nama-virtual-env # if using conda
    ```

4. Install packages

   ```sh
   pip install -r requirements.txt
   ```
   
5. Run the project
   
    **Run Streamlit**

    ```sh
    streamlit run app.py
    ```

<p align="right"><a href="#">🔝</a></p>



<!-- FEATURE -->
## Feature

- [x] Contextual understanding
- [x] Multi-language Support
    - [x] English
    - [x] Indonesian
- [x] Add documents

<p align="right"><a href="#">🔝</a></p>

<!-- ARCITECTURE -->
## Arcitecture

<p align="center">
  <img src="image\arcitecture.png" alt="Image">
</p>

<p align="right"><a href="#">🔝</a></p>


<!-- REFERENCE -->
## Reference

### GitHub Repositories
- [OpenAI Knowledge Graph Streamlit App](https://github.com/leannchen86/openai-knowledge-graph-streamlit-app/blob/main/openaiKG.ipynb) - Repository containing a Streamlit application for generating a knowledge graph using OpenAI's language model.
- [KnowledgeGraphLLM](https://github.com/projectwilsen/KnowledgeGraphLLM) - Project repository focusing on creating knowledge graphs with language models.
- [Ollama](https://github.com/ollama/ollama) - Repository providing resources for deploying and managing LLM-based applications.

### Neo4j Setup
- [Neo4J Database Setup](https://console.neo4j.io/) - Console for setting up and managing a Neo4j database, useful for knowledge graph storage and querying.

### Research Papers
- [GraphRAG: Unlocking LLM Discovery on Narrative Private Data (Microsoft)](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/) - Blog detailing Microsoft's approach to using language models with private, narrative-based data.
- [Paper: Large Language Models in Knowledge Graphs (arXiv: 2307.03172)](https://arxiv.org/pdf/2307.03172.pdf) - Research paper on the application of LLMs in knowledge graph generation and reasoning.
- [Paper: Enhanced Reasoning with Graph Neural Networks (arXiv: 2311.07509)](https://arxiv.org/pdf/2311.07509.pdf) - A paper exploring advanced reasoning techniques in large language models, using graph neural networks.

### LangChain Documentation
- [LangChain Documentation Overview](https://python.langchain.com/docs/how_to/) - Official documentation for LangChain, a framework for building applications with language models.
- [Recursive Text Splitter](https://python.langchain.com/docs/how_to/recursive_text_splitter/) - Guide on splitting text recursively for processing in LangChain.
- [Few-Shot Examples](https://python.langchain.com/docs/how_to/few_shot_examples/) - Documentation on using few-shot learning examples in LangChain.
- [QA with Chat History](https://python.langchain.com/docs/tutorials/qa_chat_history/) - Tutorial on maintaining chat history context for question-answering applications.
- [Neo4j and LangChain Integration](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/) - Instructions on integrating LangChain with Neo4j for graph-based data applications.
- [Constructing Graphs for Knowledge Applications](https://python.langchain.com/v0.1/docs/use_cases/graph/constructing) - Use case documentation on building graphs with LangChain for knowledge-based applications.

<p align="right"><a href="#">🔝</a></p>
