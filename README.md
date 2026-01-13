# Proposal Generator Agent
An agent that generates automatically cover messages based on previous projects, resume, and other details about the freelancer using the power of RAG and Open AI agent SDK.

## Setup

 ### Create and activate a virtual environment:

If you don't already have UV, [install it](https://pydevtools.com/handbook/how-to/how-to-install-uv/).
Then, in the root of the project, execute the following commands:

```
uv venv
venv\Scripts\activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Create a `.env` file in the project root (the app uses `python-dotenv` to load env vars). At minimum set the keys for whichever providers you plan to use. Example:

```
OPENAI_API_KEY=sk-...your-openai-key...
```

### Initialize Data Folder
The data folder contains personal information such as projects, resume, and other relevant details that will be used by the agent to generate proposals. To set up your local data, follow these steps:

1. Create  `data` folder in the root directory of the project if it doesn't exist already.
2. Inside the `data` folder, you can group your files into subfolders for better organization.
```
Example:
data/
    ├── about-me/
    │   └── resume.pdf
    └── projects/
        └── my-app/
            └── readme.md
```
3. Create `data.json` file.
4. Populate the `data.json` file with your personal information following the structure below:

```json
[
    {
        "name": "Resume",
        "path": "data/about-me/resume.pdf",
        "type": "pdf",
        "metadata": {
            "category": "About Me"
        }
    },
    {
        "name": "My App",
        "path": "data/projects/my-app/readme.md",
        "type": "text",
        "metadata": {
            "category": "Project",
            "name": "My App",
            "purpose": "personal",
            "visibility": "private",
            "technologies": ["Python", "AI", "OpenAI", "RAG"]
        }
    },
]
```

### Setup Vector Database
After initializing your data folder, you need to create and populate the vector database that will be used by the agent for RAG (Retrieval-Augmented Generation). Follow these steps:

1. **Run the Vector Database Setup Notebook**
   Open and execute the notebook `notebooks/vector_db_settings.ipynb`. This notebook will:
   - Load all documents from your `data.json` configuration
   - Split documents into chunks for optimal retrieval
   - Generate embeddings using OpenAI's `text-embedding-3-large` model
   - Store the embeddings in a ChromaDB vector database at `chroma_db/`

   The notebook automatically processes different file types (PDF and text) and preserves metadata including categories, technologies, and other custom fields.

2. **Verify the Database**
   After running the notebook, you should see a `chroma_db/` folder in your project root. The notebook includes test cells at the end to verify the database is working correctly with similarity searches and metadata filtering.

**Note:** If you update your data files or `data.json`, you'll need to re-run the notebook to refresh the vector database. The notebook automatically deletes and recreates the database each time it runs.
