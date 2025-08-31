# Agriculture Chatbot

A simple Streamlit-based chatbot interface for interacting with an agriculture knowledge base using a retrieval-augmented agent.

## Features

- Chatbot interface powered by Streamlit
- Uses a retrieval tool as the only knowledge source (vectorstore)
- If information is not in the knowledge base, the bot responds accordingly
- Loading animation while generating responses

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the root directory.
    - Add your OpenAI API key:
      ```
      OPENAI_API_KEY=your_openai_api_key
      ```
    - (Optional) Add other keys as needed for embeddings.

4. **Prepare the vectorstore**:
    - Ensure the `app/agriculture_chromaV2/` directory contains the vectorstore files.
    - The retriever tool is configured in `app/tool.py`.

## Running the App

Start the Streamlit app with:

```bash
streamlit run app/main.py
```

The chatbot interface will open in your browser. Type your questions about agriculture; the bot will answer using only the knowledge base.

## Project Structure

- `app/main.py` — Streamlit chatbot interface
- `app/agent.py` — CLI agent (for testing/debugging)
- `app/tool.py` — Retriever tool and vectorstore setup
- `requirements.txt` — Python dependencies
- `.env` — Environment variables (not tracked in git)
- `.gitignore` — Files and directories to ignore in git

## Notes

- The agent will only answer questions using the retriever tool. If the answer is not found, it will respond:  
  _"Sorry, that information is not currently available in the knowledge base."_
- Make sure your vectorstore is up to date for best results.

## License

MIT License