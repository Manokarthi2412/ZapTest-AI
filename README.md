# ZapTest AI  

**ZapTest AI** is an AI-powered API testing and documentation generation tool. Designed for developers and QA engineers, ZapTest AI streamlines the process of testing APIs, generating detailed test cases, and creating comprehensive API documentation.  

## Features  

- **Automated Test Case Generation**: Leverages AI through the `TestCraft.py` module to generate intelligent test cases for your APIs.  
- **API Documentation Generation**: Uses the `DocAgent.py` module, powered by LLMs, to create detailed and accurate API documentation.  
- **Route Extraction**: Analyzes Flask files using the `Extract.py` module to identify API routes automatically.  
- **API Testing**: Tests previously generated cases via the `testApi.py` module.  
- **User-Friendly Interface**: Built with Streamlit in `app.py`, providing an intuitive and seamless experience.  

---

## Project Structure  

- **`app.py`**: Streamlit app for the user interface.  
- **`constant.py`**: Stores API keys and configuration constants.  
- **`DocAgent.py`**: Connects to LLM to generate API documentation.  
- **`TestCraft.py`**: Connects to LLM to generate intelligent test cases.  
- **`testApi.py`**: Tests APIs using the previously generated test cases.  
- **`Extract.py`**: Extracts API routes from user-uploaded Flask files.  

## DEMO 

https://vimeo.com/1030252174?share=copy#t=0 

