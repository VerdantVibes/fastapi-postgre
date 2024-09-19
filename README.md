# Report Generation Platform Backend Service

Welcome to the backend service of our Report Generation Platform! This powerful service automates research and report generation by searching internal documents, the web, user-uploaded files, and specified URLs, producing a comprehensive report with accurate citations.

## 🌟 Key Features

### 📈 Report Generation

Effortlessly generate reports by harnessing data from multiple sources:

1. **User Input**: Define your target audience, report objectives, and other relevant details.
2. **Automated Research**: The system conducts four types of research in parallel:
   - **Internal Documents Search**: Leverage our database via Azure AI Search.
   - **Web Search**: Utilize Tavily Search Engine for the most relevant online data.
   - **User-Specified URLs**: Fetch data from URLs provided by you using Exa API.
   - **User-Uploaded Files**: Perform semantic search on your uploaded documents using FAISS.
3. **Ranking**: Rank all retrieved chunks using a Large Language Model (LLM).
4. **Selection and Generation**: Pass the top 20 chunks to LLM for report generation, with optional manual selection.
5. **Editing**: Manually edit reports using a Tiptap editor.

### 🧠 AI Assistant

Our AI assistant is equipped to answer your queries using several advanced tools, and can even create charts based on your requirements:

- **Tavily Search Engine**: For the latest web data.
- **Azure AI Search**: To search internal document databases.
- **Exa API**: For extracting information from user-specified URLs.
- **HighChart**: For creating visualizations.

You can explore our demo video here: [AI Assistant Demo](https://app.screencast.com/k3V1ZZwbBG98v)

## 🛠 Technologies

1. **FastAPI**: Robust RESTful API framework
2. **PostgreSQL**: Reliable and powerful database
3. **Alembic**: Easy database migration
4. **Azure OpenAI**: Advanced large language model
5. **Azure AI Search**: Comprehensive vector database
6. **Tavily Search Engine**: State-of-the-art search engine
7. **Langfuse**: For LLM tracing and prompt management
8. **Docker & Docker Compose**: Simplified container management

## 🚀 Getting Started

Follow these steps to run the server locally:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ulrich1031/fastapi-azure-postgres-nginx.git
    ```

2. **Build Docker Container**:
    ```bash
    make runBuildLocalDocer
    ```

3. **Navigate to Backend Directory**:
    ```bash
    cd backend
    ```

4. **Set Environment Variables**:
    - Copy `env.example` and rename it to `.env.local`
    - Replace the placeholder values with your actual credentials.

5. **Run the Server**:
    ```bash
    make runLocal
    ```

    The server will be up at `http://localhost:8001`, and you can test the endpoints at `http://localhost:8000/docs`.

![Demo Video](https://app.screencast.com/MoAlIaayeseXs)

---

Enjoy using the Report Generation Platform! 🚀
```

Feel free to reach out if you have any questions or need further assistance. Happy developing! 😊
```