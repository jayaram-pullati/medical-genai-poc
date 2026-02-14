## 🏥 Medical Drug GenAI RAG POC
### 📌 Overview

This project demonstrates a Retrieval-Augmented Generation (RAG) architecture for medical drug information using AWS-native services.

The system retrieves drug-related information from enterprise data sources and generates grounded responses with citations to ensure safety and traceability.

### 🏥 Architecture
```
                 ┌───────────────┐
                 │   React UI    │ (Amplify hosted)
                 └───────┬───────┘
                         │
                  HTTPS Request
                         │
                 ┌───────────────┐
                 │  FastAPI API  │
                 └───────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          │                              │
   Embed Question                   Drug Lookup
 (Bedrock Embedding)             (DynamoDB metadata)
          │                              │
          └──────────────┬──────────────┘
                         │
               OpenSearch (kNN vector search)
                         │
                Retrieve top-k chunks
                         │
                Bedrock (Generate answer)
                         │
                Answer + Citations

```

#### Components

- S3 – Stores drug labels, PDFs, and documents

- DynamoDB – Stores structured drug metadata and versioning

- OpenSearch – Stores chunked text + embeddings for semantic retrieval

- AWS Bedrock 
   * Embedding model for vector generation
   * Foundation model for answer generation

- FastAPI Backend – Handles API requests

- React UI (Amplify-ready) – Frontend interface

### 🏗️ High-Level Flow
```
React UI (Amplify Hosted)
        ↓
FastAPI Backend (Python)
        ↓
Embedding (AWS Bedrock)
        ↓
OpenSearch (kNN Vector Retrieval)
        ↓
LLM Generation (AWS Bedrock)
        ↓
Answer + Citations

```
#### Supporting services:

- S3 – Document storage

- DynamoDB – Structured metadata & version control

- OpenSearch – Vector search

- Bedrock – Embedding + LLM

- Glue – Optional ETL

- Amplify – Frontend hosting

### AWS Services and Their Responsibilities

#### 🔹 Amazon S3 – Document Storage

**Purpose:** Store raw drug documentation.

**Data stored:**

- Drug labels

- Regulatory PDFs

- Monographs

**Usage in system:**

- Ingestion service reads documents

- Extracts and chunks text

- Prepares content for embedding

#### 🔹 Amazon DynamoDB – Structured Metadata

**Purpose:** Store structured drug data and enforce version control.

**Data stored:**

- drugId

- generic/brand name

- strength

- form

- version

- approval status

- effective date

**Usage in system:**

- Exact drug lookup

- Version filtering

- Approval filtering

- Ensuring latest label usage

#### 🔹 Amazon OpenSearch – Semantic Retrieval

**Purpose:** Retrieve relevant drug content using vector similarity.

**Data stored per chunk:**

- text

- embedding vector

- drugId

- version

- approval flag

**Usage in system:**

- kNN vector search for semantic similarity

- Metadata filtering (approved & latest version)

- Hybrid search capability (keyword + vector)

#### 🔹 Amazon Bedrock – GenAI Engine

Bedrock is used in two distinct roles:

**1. Embedding Model**

Converts:

- Drug text chunks → embeddings

- User question → embedding

Required for vector search.

**2. Foundation Model (LLM)**

Generates:

- Final answer

- Summary of retrieved content

- Structured response

Strict prompt enforcement ensures no hallucination.

#### 🔹 AWS Glue (Optional ETL Layer)

Used for:

- Cleaning inconsistent drug data

- Converting legacy formats

- Scheduled ingestion jobs

Prepares data before indexing.

#### 🔹 AWS Amplify (Frontend Hosting)

Used for:

- Hosting React UI

- CI/CD for frontend

- Optional Cognito authentication

Does not handle GenAI logic.

### Detailed Query Flow

**1.** User submits question.

**2.** Backend embeds question using Bedrock embedding model.

**3.** OpenSearch performs kNN vector search.

**4.** Retrieval is filtered to:

   - approved = true
   - latest version only

**5.** Retrieved chunks sent to Bedrock LLM.

**6.** LLM generates answer strictly from provided context.

**7.** API returns:

- Answer

- Citations (doc_id, chunk_id)

### Hallucination Prevention Strategy

To ensure medical safety:

- RAG architecture (no direct LLM usage)

- Strict grounding prompt

- No-answer fallback if context insufficient

- Version filtering

- Approved-only filtering

- Citation-based response

- Low temperature configuration

### Scalability Strategy

- Batch embedding generation

- Async ingestion pipeline (SQS recommended)

- OpenSearch cluster auto-scaling

- API rate limiting

- Caching frequent queries

### Security Considerations

- IAM least privilege

- KMS encryption for S3 & DynamoDB

- Private networking (VPC endpoints)

- Optional Cognito authentication

- Audit logging for traceability

### Why RAG Instead of Direct LLM?

Direct LLM:

- Relies on pre-trained knowledge

- May hallucinate

- Not traceable

RAG:

- Uses enterprise drug data

- Grounded responses

- Citation support

- Safer for medical domain

### Future Enhancements

- Hybrid search (keyword + vector reranking)

- Drug interaction reasoning

- Role-based access control

- Audit trail analytics

- Fine-tuned medical model (if required)