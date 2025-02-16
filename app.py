import os
import json
import asyncio
import streamlit as st
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy

# -----------------------------
# Async scraping function
# -----------------------------
async def run_scrape(url: str, instruction: str, input_format: str, provider: str, api_key: str, schema: dict):
    llm_strategy = LLMExtractionStrategy(
        provider=provider,
        api_token=api_key,
        schema=schema,
        extraction_type="schema",
        instruction=instruction,
        chunk_token_threshold=1000,
        overlap_rate=0.0,
        apply_chunking=True,
        input_format=input_format,
        extra_args={"temperature": 0.0, "max_tokens": 800}
    )

    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    browser_cfg = BrowserConfig(headless=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url=url,
            config=crawl_config
        )

    return result, llm_strategy

# -----------------------------
# Helper to run async function
# -----------------------------
def scrape(url: str, instruction: str, input_format: str, model_choice: str, api_key: str, schema: dict):
    provider_mapping = {
        "gpt-4o-mini": "openai/gpt-4o-mini",
        "gpt-4o": "openai/gpt-4o",
        "ollama/llama2": "ollama/llama2",
        "ollama&llama3": "ollama/llama3"
    }
    provider = provider_mapping.get(model_choice, "openai/gpt-4o-mini")
    return asyncio.run(run_scrape(url, instruction, input_format, provider, api_key, schema))

# -----------------------------
# Sidebar: Configuration and Instructions
# -----------------------------
st.sidebar.info(
    """
    **This app allows you to:**

    - **Select a Model,**
    - **Enter your OpenAI API Key (if applicable),**
    - **Define a Schema for extraction,** and
    - **Provide a URL along with extraction instructions.**

    When you click **Scrape**, the crawler runs with your parameters and returns the scraped JSON data.
    """
)

st.sidebar.header("Configuration")

model_choice = st.sidebar.selectbox(
    "Select Model",
    options=["gpt-4o-mini", "gpt-4o", "ollama/llama2", "ollama&llama3"]
)

api_key = st.sidebar.text_input("OpenAI API Key", type="password")

schema_input = st.sidebar.text_area(
    "Schema Definition (in JSON)",
    value='{\n    "name": "str",\n    "price": "str"\n}',
    height=150
)

# -----------------------------
# Main UI
# -----------------------------
st.title("Web Scraper with LLM Extraction Strategy")

instruction = st.text_input(
    "Extraction Instruction",
    value="Extract all product objects with 'name' and 'price' from the content."
)

input_format = st.text_input("Input Format", value="html")

url = st.text_input("URL to Scrape", value="https://www.trendyol.com/cep-telefonu-x-c103498")

# -----------------------------
# Run Scraping on Button Click
# -----------------------------
if st.button("Scrape"):
    try:
        schema_dict = json.loads(schema_input)
    except Exception as e:
        st.error(f"Invalid JSON in Schema Definition: {e}")
    else:
        if not api_key:
            st.warning("The API key is empty. Make sure to enter your API key if required.")
        with st.spinner("Scraping..."):
            result, llm_strategy = scrape(url, instruction, input_format, model_choice, api_key, schema_dict)
        if result.success:
            try:
                data = json.loads(result.extracted_content)
                st.success("Scraping succeeded!")
                st.subheader("Extracted Data")
                st.json(data)
                usage_info = llm_strategy.show_usage()
                if usage_info:
                    st.subheader("LLM Usage Info")
                    st.text(usage_info)
            except Exception as e:
                st.error(f"Error parsing the extracted content: {e}")
        else:
            st.error(f"Scraping failed: {result.error_message}")
