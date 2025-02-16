# Web Scraper with LLM Extraction Strategy

This project is a simple web scraping application built with [Streamlit](https://streamlit.io) that leverages the `crawl4ai` library to extract structured data from web pages using various large language models (LLMs). Users can dynamically configure the extraction process by selecting a model, entering an API key, defining a custom schema, and providing extraction instructions.

## Features

- **Model Selection:** Choose from multiple LLM providers (e.g. `gpt-4o-mini`, `gpt-4o`, `ollama/llama2`, `ollama&llama3`).
- **API Key Input:** Securely enter your OpenAI API key (or other required keys) directly in the sidebar.
- **Schema Definition:** Define a JSON schema for data extraction (default schema extracts product name and price).
- **Custom Extraction Instructions:** Provide tailored extraction instructions to suit your target webpage.
- **Asynchronous Crawling:** Uses asynchronous functions for efficient web crawling and data extraction.
- **Interactive UI:** Built with Streamlit for a user-friendly interface.

## Prerequisites

- Python 3.8 or higher
- [Streamlit](https://streamlit.io)
- [crawl4ai](https://github.com/your-repo/crawl4ai) (or ensure the library is installed)

## Installation

1. **Clone the Repository:**

- git clone https://github.com/yourusername/web-scraper-llm.git
  
2. **Create a Virtual Environment (Optional but Recommended)**:

- python -m venv venv
- source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies:**

- Ensure you have a requirements.txt file with at least the following:

* streamlit
* crawl4ai
Then run:

- pip install -r requirements.txt
- streamlit run app.py
  
4. **Configuration**
- API Key:
If using a model that requires an API key (such as OpenAI's GPT models), either set the environment variable OPENAI_API_KEY or enter it in the sidebar when running the app.

- Schema Definition:
The sidebar allows you to define a JSON schema for extraction. The default is:

{
    "name": "str",
    "price": "str"
}
