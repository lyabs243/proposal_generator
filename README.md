# Proposal Generator Agent
An agent that generates automatically cover messages based on previous projects, resume, and other details about the freelancer using the power of RAG and Open AI agent SDK.

## Setup

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
