# Customer Executive Chatbot

A chatbot solution for customer executive interactions.
Used open api and RAG(Retrieval-Augmented Generation) to read insurance documents and answer customer queries based on the docs.

## Features

- Automated customer support
- Natural language processing
- Easy integration


## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/CustomerExecutiveChatbot.git
    cd CustomerExecutiveChatbot
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables:**
    - Copy `.env.example` to `.env` and update values as needed.

4. **Run the application django backend:**
    
    ```
    cd chatbot
    python manage.py runserver
    ```
5. **Run streamlit frontend:**
    ```
    cd chatbot
    streamlit run streamlit_app.py
    ```

## Usage

- Access the chatbot via `http://localhost:8000` in your browser.
- Interact with the chatbot using the provided UI.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request.

##

DEMO URL: https://customersupportaichatbot-gxbcnvfunhham7pqznb4nd.streamlit.app/