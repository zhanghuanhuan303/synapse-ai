# Synapse Architecture

## Overview

Synapse is designed as a modular, extensible system for intelligent document processing. The architecture is divided into several layers, each responsible for a specific aspect of the document transformation pipeline.

## High-Level Architecture
The architecture is a series of concentric, interacting layers, moving from user interaction down to infrastructure. Here is the system's blueprint:
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION LAYER                    │
│  Provides the interface for idea capture and document review │
├─────────────┬──────────────┬─────────────────┬──────────────┤
│   Web App   │ Mobile Apps  │ Desktop Client  │    CLI &     │
│  (React)    │ (React Native│   (Electron)    │    API       │
│             │    / Swift)  │                 │              │
└─────────────┴──────────────┴─────────────────┴──────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                       │
│ Manages workflows, state, and communication between services │
├─────────────────────────────────────────────────────────────┤
│  ► API Gateway (REST/GraphQL/WebSocket)                     │
│  ► Real-time Sync Engine (Operational Transform / CRDTs)    │
│  ► Job Queue & Scheduler (Celery)                           │
│  ► Event Bus (for internal service communication)           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 CORE INTELLIGENCE LAYER                      │
│     The "brain" - transforms content and applies logic       │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────────────┐   │
│  │   Ingestion │ │   Analysis  │ │    Transformation    │   │
│  │  & Parsing  │ │   Engine    │ │       Engine         │   │
│  └─────────────┘ └─────────────┘ └──────────────────────┘   │
│          │               │               │                  │
│      ┌───┴───────────────┴───────────────┴────┐            │
│      │       SYNAPSE DOCUMENT MODEL            │            │
│      │  A unified, enriched content graph      │            │
│      │  representing structure, semantics,     │            │
│      │  and style intent.                      │            │
│      └─────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    RENDERING LAYER                           │
│   Generates final output via parallel, specialized paths     │
│      ┌────────────────────────────────────────┐             │
│      │     DUAL-PATH SYNAPSE ENGINE           │             │
│      │                                        │             │
│      │  ┌──────────────┐   ┌──────────────┐  │             │
│      │  │   PATH A:    │   │   PATH B:    │  │             │
│      │  │ Native LaTeX │   │  Universal   │  │             │
│      │  │   Compiler   │◄──┤   Pipeline   │  │             │
│      │  │              │   │  (via Pandoc)│  │             │
│      │  └──────────────┘   └──────────────┘  │             │
│      │          │                  │          │             │
│      │          └───────┬──────────┘          │             │
│      │                  ▼                     │             │
│      │        Template & Style Engine         │             │
│      └────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                      │
│  Provides persistent storage, compute, and operational glue  │
├─────────────┬──────────────┬─────────────────┬──────────────┤
│  PostgreSQL │    Redis     │  Object Store   │   Search     │
│  (Primary   │  (Cache &    │   (S3/OSS)      │  (Elastic)   │
│   Database) │   Sessions)  │                 │              │
└─────────────┴──────────────┴─────────────────┴──────────────┘

## Core Components

### 1. Parser Module
The parser is responsible for converting input documents (in various formats) into an internal document object model (DOM).

**Supported Input Formats:**
- Plain Text (.txt)
- Markdown (.md)
- LaTeX (.tex)
- Microsoft Word (.docx) - planned

**Dual-Path Architecture:**
- **Path A (Direct)**: For formats that map well to LaTeX (e.g., LaTeX, Markdown), we use a direct transformation.
- **Path B (Adaptive)**: For complex or less structured formats (e.g., Word), we first convert to a Markdown intermediate, then use Pandoc for further conversion.

### 2. Semantic Analysis Module
This module uses NLP techniques to understand the document's structure and content.

**Key Functions:**
- Identify document sections (abstract, introduction, conclusion, references)
- Detect citation patterns and reference lists
- Analyze writing style and suggest improvements
- Extract key concepts and their relationships

**Planned Models:**
- Pre-trained BERT for sequence classification
- spaCy for entity recognition and dependency parsing
- Custom models for academic document structure

### 3. Renderer Module
Converts the internal DOM into output formats.

**Supported Output Formats:**
- LaTeX (with compilation to PDF)
- HTML (for web preview)
- Microsoft Word (.docx) - planned
- ePub - planned

**Dual-Path Rendering:**
- **Path A (LaTeX)**: Direct compilation using a containerized LaTeX environment
- **Path B (Pandoc)**: Use Pandoc for conversions to and from multiple formats

### 4. Template System
Synapse uses templates to control the visual appearance of documents.

**Template Types:**
- **LaTeX Templates**: Class files and style files
- **HTML/CSS Templates**: For web preview
- **Word Templates**: .dotx files for Word output

**Template Management:**
- System-provided templates
- User-uploaded custom templates
- Template marketplace (future)

## Data Flow

1. **Upload**: User uploads a document via web, mobile, or API.
2. **Parsing**: The document is parsed into the internal DOM.
3. **Analysis**: Semantic analysis enriches the DOM with structural and content metadata.
4. **Template Selection**: User selects a template (or auto-selection based on content).
5. **Rendering**: The DOM is rendered into the target format using the selected template.
6. **Compilation**: For LaTeX, the output is compiled to PDF in a Docker container.
7. **Delivery**: The final document is returned to the user.

## Technology Stack

### Backend
- **Language**: Python 3.10+
- **Web Framework**: FastAPI (for async support and automatic OpenAPI documentation)
- **Task Queue**: Celery with Redis as broker
- **Database**: PostgreSQL (primary), Redis (cache)
- **File Storage**: Cloud object storage (AWS S3, Alibaba OSS, or self-hosted MinIO)

### Frontend
- **Web**: React with TypeScript, Tailwind CSS
- **Mobile**: React Native for cross-platform (or native Swift/Kotlin if needed)
- **Mini Programs**: Taro for cross-platform mini programs (WeChat, Alipay, etc.)

### Infrastructure
- **Containerization**: Docker for service isolation, especially LaTeX compilation
- **Orchestration**: Kubernetes (for production) or Docker Compose (for development)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana, ELK Stack

## Security Considerations

- **Document Isolation**: Each document processing job runs in a separate Docker container.
- **Resource Limits**: CPU, memory, and time limits on compilation jobs.
- **Input Validation**: Strict validation of uploaded files to prevent injection attacks.
- **Data Privacy**: User documents are encrypted at rest and in transit.

## Scalability

The system is designed to be horizontally scalable:
- Stateless API servers can be scaled based on load.
- Celery workers can be added to handle more document processing jobs.
- Database read replicas for high read throughput.

## Deployment

We provide multiple deployment options:
1. **Cloud SaaS**: Fully managed service by Synapse.
2. **Self-Hosted**: Docker Compose or Kubernetes manifests for on-premises deployment.
3. **Hybrid**: Some components in the cloud, some on-premises.

## Future Extensions

- **Real-time Collaboration**: Multiple users editing the same document.
- **Version Control**: Git-like versioning for documents.
- **Plugin System**: Third-party extensions for additional formats, analysis, and rendering.
