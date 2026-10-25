# Project 46: Printing Services Assistant

A **Flask-based AI-powered Printing Services Assistant** that helps customers understand printing policies, retrieve answers from a knowledge base using Retrieval-Augmented Generation (RAG), and calculate printing costs using a deterministic calculator. The project uses **Google Gemini** for embeddings and response generation, with **ChromaDB** for persistent vector storage.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Architecture](#project-architecture)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Printing Cost Rules](#printing-cost-rules)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Questions](#example-questions)
- [Testing](#testing)
- [Promptfoo Evaluation](#promptfoo-evaluation)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)

## Overview

The Printing Services Assistant is designed to provide quick, consistent answers to common printing-related questions and estimate the cost of print orders.

It combines a knowledge-based question-answering system with a rule-based calculator. Customers can ask about printing specifications, collection procedures, printing charges, and binding costs without manually searching through policy documents.

The application uses RAG to retrieve relevant information from local knowledge documents before generating an answer. ChromaDB stores document embeddings persistently, reducing the need to recreate embeddings for unchanged documents on every request.

## Key Features

- **AI-Powered Question Answering:** Answers printing-related questions using retrieved knowledge documents.
- **Retrieval-Augmented Generation (RAG):** Grounds responses in relevant content from the knowledge base.
- **Persistent Vector Database:** Uses ChromaDB to store and retrieve document embeddings.
- **Google Gemini Integration:** Generates embeddings and natural-language responses using configured Gemini models.
- **Printing Cost Calculator:** Calculates printing charges, paper requirements, binding charges, and total estimated cost.
- **Printing Options:** Supports black-and-white or colour printing, single-sided or double-sided printing, and optional binding.
- **Source References:** Returns the knowledge-document sources used for an answer.
- **Input Validation:** Rejects invalid page and copy counts.
- **Fallback Model Support:** Allows configured alternative Gemini generation models when the primary model fails.
- **Health Check Endpoint:** Provides a simple endpoint to check whether the Flask application is responding.
- **Automated Testing:** Supports tests using pytest.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application and API framework |
| Google Gemini API | Text embeddings and AI response generation |
| ChromaDB | Persistent vector database |
| NumPy | Numerical operations where required |
| python-dotenv | Environment variable management |
| pytest | Automated testing |
| Promptfoo | Optional RAG evaluation |

## Project Architecture

The application consists of the following major components:

1. **Flask Application (`app.py`)**  
   Handles web requests, renders the user interface, validates calculator inputs, and exposes API endpoints.

2. **RAG Module (`rag.py`)**  
   Loads knowledge documents, splits content into chunks, creates embeddings, retrieves relevant information from ChromaDB, and generates grounded answers using Gemini.

3. **Printing Calculator (`calculator.py`)**  
   Calculates printing costs and paper requirements using predefined pricing rules.

4. **Knowledge Base (`knowledge/`)**  
   Stores the text documents containing printing specifications, order guidance, and collection policies.

5. **ChromaDB Storage (`chroma_db/`)**  
   Stores the persistent vector collection used for semantic retrieval.

## Project Structure

The project is organised approximately as follows. Your actual project may contain additional files.

```text
project46_printing_assistant/
│
├── app.py
├── rag.py
├── calculator.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── promptfooconfig.yaml
│
├── knowledge/
│   ├── print_specifications.txt
│   ├── print_order_guide.txt
│   └── collection_policy.txt
│
├── chroma_db/
│   └── Persistent vector database files
│
├── templates/
│   └── index.html
│
└── tests/
    └── Test files
```

**Note:** The exact test filenames and optional configuration files depend on your implementation. Keep your actual filenames and folder structure consistent with your code.

## How It Works

### 1. Knowledge-Based Question Answering

1. The customer submits a printing-related question.
2. The Flask application passes the question to the RAG module.
3. The RAG module creates an embedding for the question using Gemini.
4. ChromaDB retrieves semantically relevant document chunks.
5. The retrieved content is supplied to the configured Gemini generation model.
6. The assistant generates an answer based on the retrieved context.
7. The API returns the answer and available source information.

### 2. Printing Cost Estimation

1. The customer enters the number of pages per copy and number of copies.
2. The customer selects black-and-white or colour printing.
3. The customer selects single-sided or double-sided printing.
4. The customer specifies whether binding is required.
5. The calculator validates the inputs and applies the pricing rules.
6. The application displays the estimated printing charge, paper-sheet count, binding charge, and total cost.

The calculator uses deterministic rules rather than asking the language model to perform the final price calculation.

## Printing Cost Rules

The application uses the following configured pricing rules:

| Item | Rule |
|---|---|
| Black-and-white printing | ₹2 per printed side |
| Colour printing | ₹8 per printed side |
| Optional binding | ₹30 per copy |
| Single-sided printing | One sheet per page per copy |
| Double-sided printing | One sheet for every two pages per copy, rounding up |

### Calculation Example

Suppose a customer requests:

- Pages per copy: 5
- Number of copies: 3
- Printing mode: Black and white
- Printing sides: Double-sided
- Binding: Required

**Calculation:**

- Total printed sides = 5 × 3 = 15
- Paper sheets = ceiling(5 ÷ 2) × 3 = 9
- Printing charge = 15 × ₹2 = ₹30
- Binding charge = 3 × ₹30 = ₹90
- Total estimated cost = ₹30 + ₹90 = **₹120**

Double-sided printing reduces the number of paper sheets, but it does not reduce the printing charge under these pricing rules.

### Second Example

For 4 pages per copy, 2 copies, colour printing, single-sided, without binding:

- Total printed sides = 4 × 2 = 8
- Paper sheets = 8
- Printing charge = 8 × ₹8 = ₹64
- Binding charge = ₹0
- Total estimated cost = **₹64**

These are estimates based on the application's configured rates. Actual charges may differ if the service provider changes its pricing.

## Installation and Setup

### Prerequisites

Install the following before running the application:

- Python compatible with the installed dependencies
- pip
- A Google Gemini API key
- Internet access for Gemini API requests

### Step 1: Open the Project Folder

Open PowerShell or the VS Code terminal and navigate to the project directory:

```powershell
cd C:\Users\mohan\Downloads\project46_printing_assistant\project46_printing_assistant
```

Adjust the path if your project is stored elsewhere.

### Step 2: Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the commands through Command Prompt instead, or use an appropriate execution-policy setting for your environment.

### Step 3: Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure the Environment

Create a `.env` file in the project root and configure the variables described below. Do not upload your real API key to a public repository.

### Step 5: Verify the Project Files

Make sure that the application files, templates, knowledge documents, and calculator module exist in the expected locations.

## Environment Configuration

Example `.env` configuration:

```env
GEMINI_API_KEY=your_gemini_api_key_here

GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_MODEL_FALLBACKS=gemini-3.6-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-001

CHROMA_DIR=chroma_db
RAG_TOP_K=4
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=150

FLASK_DEBUG=true
```

Replace the example API key with your own valid key. Do not share it publicly.

The model names above reflect the example configuration used during development. If a model becomes unavailable to your account, configure a model currently supported by your Gemini API access.

If your knowledge documents are not stored in the default `knowledge/` directory, configure `KNOWLEDGE_DIR` with the correct path.

For example:

```env
KNOWLEDGE_DIR=knowledge
```

The application should load environment variables before creating the Gemini client.

## Running the Application

From the project root, activate the virtual environment and run:

```powershell
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

### Health Check

Open the following URL:

```text
http://127.0.0.1:5000/health
```

A successful response should resemble:

```json
{
  "status": "ok",
  "service": "project46_printing_assistant"
}
```

### API Documentation

The application currently exposes its routes through Flask. Unless a separate documentation interface has been implemented, there is no automatic Swagger UI at `/docs`.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Displays the printing assistant interface |
| POST | `/ask` | Answers a question using the RAG system |
| POST | `/estimate` | Calculates an estimated printing cost |
| GET | `/health` | Checks application availability |

### POST `/ask`

Example JSON request:

```json
{
  "question": "What should customers retain for collection?"
}
```

The endpoint returns the RAG answer and may include source references, retrieved-chunk information, model details, and vector-store metadata according to the current implementation.

### POST `/estimate`

The endpoint accepts form data for the printing calculator.

Expected fields:

- `pages`: Number of pages per copy
- `copies`: Number of copies
- `colour_mode`: `black_white` or `colour`
- `double_sided`: `yes` when double-sided printing is selected
- `binding_required`: `yes` when binding is required

The calculator validates the inputs and returns the rendered interface with the estimated result or a validation error.

## Example Questions

Use these questions to test the knowledge-based assistant.

### Supported Questions

1. What should customers retain for collection?
2. What is the black-and-white printing charge per side?
3. What is the colour printing charge per side?
4. How much does optional binding cost per copy?
5. Does double-sided printing reduce the printing charge?
6. How are paper sheets calculated for double-sided printing?

### Out-of-Scope Questions

1. What is my current bank account balance?
2. Has my document finished printing?
3. Can you track my live print order?
4. Can you access my personal files?
5. What is the weather today?

For out-of-scope questions, the assistant should avoid inventing information or claiming access to systems it does not have. Its response should clearly explain the relevant limitation.

## Testing

Run the automated test suite from the project root:

```powershell
python -m pytest -q
```

The project previously reported:

```text
7 passed, 1 skipped
```

That result reflects an earlier test run. Run the command again after making changes to confirm the current result.

### Manual Testing Checklist

- [ ] The home page loads successfully.
- [ ] The health endpoint returns a successful response.
- [ ] A supported knowledge question returns a relevant answer.
- [ ] The answer includes source information when available.
- [ ] The printing calculator returns the expected cost.
- [ ] Zero or invalid page counts are rejected.
- [ ] Invalid copy counts are rejected.
- [ ] Out-of-scope questions do not produce fabricated claims.
- [ ] ChromaDB creates and retains persistent data.
- [ ] The application handles Gemini API errors without crashing the whole server.

## Promptfoo Evaluation

Promptfoo can be used to evaluate the assistant's responses against predefined expectations.

If your project contains a `promptfooconfig.yaml` file, ensure that the Flask server is running before executing evaluations that call the local `/ask` endpoint.

Run:

```powershell
promptfoo eval --no-cache -j 1
```

The evaluation cases can cover printing prices, collection policy, double-sided printing rules, binding costs, and out-of-scope questions.

A successful evaluation should indicate that the assistant's answers satisfy the configured assertions. The exact result depends on the current configuration and model responses.

## Limitations

- The assistant relies on the knowledge documents provided in the local knowledge base.
- Answers may be incomplete if the relevant policy is missing from the documents.
- Gemini requests require a valid API key, network access, and an available model.
- ChromaDB provides persistent retrieval storage; it does not itself guarantee that generated answers are correct.
- Printing estimates use configured prices and do not represent a confirmed service-provider quote.
- The application does not actually upload, inspect, or print customer documents.
- The application does not access live order status, payment systems, or bank account information unless those integrations are implemented separately.
- The assistant should not invent information when the requested data is unavailable.

## Future Enhancements

- Add user authentication and role-based access.
- Store print orders and estimates in a database.
- Add order tracking through an authorised printing-service API.
- Add PDF upload and document page-count extraction.
- Provide downloadable cost estimates or receipts.
- Improve knowledge-document management and automatic re-indexing.
- Add logging, monitoring, and structured error reporting.
- Expand automated evaluation with more edge cases and regression tests.
- Deploy the application to a secure hosting platform.

## Conclusion

The Printing Services Assistant combines a Flask web application, Gemini-powered retrieval-augmented question answering, ChromaDB persistent vector storage, and a deterministic printing-cost calculator.

The project demonstrates how AI-based knowledge retrieval can be combined with explicit business rules to provide useful printing guidance and consistent cost estimates.

---

**Project:** Project 46 — Printing Services Assistant  
**Primary Language:** Python  
**Framework:** Flask  
**AI Integration:** Google Gemini  
**Vector Database:** ChromaDB
#   G E N E R A T I V E - A I - R A G - M O D E L -  
 #   G E N E R A T I V E - A I - R A G - M O D E L -  
 