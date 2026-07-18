# DevOps Multi-Cloud Cost Optimization & Telemetry Dashboard

An enterprise-grade, full-stack microservices application engineered to serve as a unified command pane into infrastructure asset utilization and continuous spend patterns across Amazon Web Services (AWS) and Google Cloud Platform (GCP).

---

## 🏗️ System Architecture & Event Topology

```text
                                 ┌────────────────────────────────────────────────────────┐
                                 │                   Multi-Cloud APIs                     │
                                 │     (AWS Cost Explorer API / GCP Cloud Billing API)    │
                                 └───────────────────────────┬────────────────────────────┘
                                                             │ (Python Ingestion Jobs)
                                                             ▼
                                 ┌────────────────────────────────────────────────────────┐
                                 │               MongoDB NoSQL Cluster                    │
                                 │     (Stores Normalized Historical Billing Records)     │
                                 └───────────────────────────┬────────────────────────────┘
                                                             │
                                              ┌──────────────┴──────────────┐
                                              ▼                             ▼
                                 ┌────────────────────────┐    ┌────────────────────────┐
                                 │   Python FastAPI App   │    │ Prometheus / Alertmgr  │
                                 │  (Serves JSON Data)    │    │ (Monitors Thresholds)  │
                                 └────────────┬───────────┘    └────────────┬───────────┘
                                              │                             │
                                              ▼                             ▼
                                 ┌────────────────────────┐    ┌────────────┴───────────┐
                                 │ React.js User Frontend │    │ Dual Escalation Receivers
                                 │ (Analytical Dashboards)│    └──────┬───────────┬─────┘
                                 └────────────────────────┘           │           │
                                                                      ▼           ▼
                                                       ┌────────────────┐ ┌────────────────┐
                                                       │  Slack Channel │ │ WhatsApp App   │
                                                       │ (ChatOps Feed) │ │ (Push Alerts)  │
                                                       └────────────────┘ └────────────────┘
```

---

## 🎯 Project Vision & Scope

Unmanaged cloud deployments frequently suffer from "cloud blindness," leading to thousands of dollars wasted on forgotten, idle, or oversized cloud resources. This capstone project engineers an automated multi-tenant system that tracks, isolates, and reduces cloud infrastructure costs in real-time.

### Core Objectives:
1. **Cross-Cloud Data Aggregation**: Dynamically pull multi-cloud billing line items and unstructured cost objects from vendor APIs (AWS Cost Explorer and GCP Cloud Billing).
2. **Unified Data Normalization**: Store varying cloud metrics natively into a flexible NoSQL database model, converting mixed data structures into matching records without schema overhead.
3. **Continuous Tracking & Metrics Retention**: Employ background task automation to maintain rolling historical cost logs over a custom timeframe.
4. **Active Cost Optimization & Anomaly Detection**: Analyze hardware utilization levels to actively identify under-utilized or idle instances, outputting clear cost-saving recommendations.
5. **Simultaneous Multi-Channel Budget Guardrails**: Establish automated alerting rules to instantly trigger and route over-budget incident warnings to Slack channels and mobile WhatsApp clients concurrently.

---

## 📁 Project Directory Architecture

```text
Capstone-CostMonitoring/
├── .github/workflows/
│   └── deploy.yml            # Automated CI/CD build scripts
├── alertmanager/
│   └── alertmanager.yml      # Incident notification dual-routing profile
├── prometheus/
│   ├── alert.rules.yml       # Cost metric alerting conditions
│   └── prometheus.yml        # Telemetry metrics collection configuration
├── backend/                  # Asynchronous Core Data Layer
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI Web Core and WhatsApp webhook router
│   │   ├── collectors.py     # Multi-cloud extraction and normalization loops
│   │   └── database.py       # Asynchronous MongoDB client connection pool
│   ├── requirements.txt      # Core Python application dependencies
│   └── Dockerfile            # Optimized Python microservice container blueprint
├── frontend/                 # Reactive User Presentation Interface
│   ├── src/
│   │   ├── main.jsx          # JavaScript application mount hub
│   │   └── App.jsx           # Graph analytics canvas engine
│   ├── index.html            # Web app index page template anchor
│   ├── vite.config.js        # React plugin compiler bundler instructions
│   ├── package.json          # Frontend client build and runtime manifests
│   └── Dockerfile            # Multi-stage production Nginx container file
├── docker-compose.yml        # Multi-service network orchestration matrix
├── .env                      # Hidden operational security credentials key manifest
├── .env.example              # Public structural environment template configuration
└── README.md                 # Complete documentation master report (This file)
```

---

## 🛠️ Technology Stack Matrix
- **Data Processor Web Engine**: Python 3.11 (FastAPI Framework)
- **Visual Analytics Framework**: JavaScript (React.js Client App via Vite)
- **Persistence Storage Node**: MongoDB Engine (NoSQL Document Store)
- **System Metrics Monitoring**: Prometheus Scraper Engine & Alertmanager Daemon
- **Cloud Notification Gateway**: Twilio API Ecosystem
- **Orchestration & Delivery**: Docker & Docker Compose container runtimes

---

## 💻 Local Installation & Build Sequence

### Step 1: Populate Local Configuration Credentials
Generate your workspace `.env` file at the root directory level:
```bash
cp .env.example .env
```
Open `.env` in a text editor and enter your cloud billing access tokens:
```env
MONGO_URI=mongodb://root:SecureMongoPassword123@localhost:27017/devops_metrics?authSource=admin
AWS_DEFAULT_REGION=us-east-1
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID_HERE
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
GCP_PROJECT_ID=project-55b551ca-4784-44f6-abc
GCP_ACCESS_TOKEN=YOUR_SHORT_LIVED_OAUTH_TOKEN_HERE
TWILIO_ACCOUNT_SID=YOUR_TWILIO_ACCOUNT_SID_HERE
TWILIO_AUTH_TOKEN=YOUR_TWILIO_AUTH_TOKEN_HERE
WHATSAPP_TARGET_NUMBER=YOUR_MOBILE_NUMBER_HERE
```

### Step 2: Build and Launch the Orchestrated Network Topology
Compile container assets and launch the entire full-stack graph network in background mode:
```bash
docker-compose up -d --build
```

### Step 3: Seed the Database Matrix Manually
Trigger the background multi-cloud data collection script inside your running backend API container to pull live tracking metrics into MongoDB:
```bash
docker-compose exec backend python app/collectors.py
```

### Step 4: Verify Exposed Management Interfaces
Open your web browser to interact with the runtime application layers:
- 🖥️ **React DevOps Graphic Canvas Dashboard Panel**: `http://localhost:3000`
- ⚙️ **FastAPI Interactive API Swagger Docs**: `http://localhost:8000/docs`
- 📈 **Prometheus Data Scraper Engine Interface**: `http://localhost:9090`
- 🚨 **Alertmanager Incident Alert Router Panel**: `http://localhost:9093`

---

## 🎓 Step-by-Step Viva Presentation Script (3-Minute Presentation)

Use this structure to walk your evaluators through the running dashboard during your project defense:

### 1. Introduction & Project Scope [0:00 - 0:45]
> *"Good morning, evaluators. This capstone presents a **DevOps Multi-Cloud Cost Optimization & Telemetry Dashboard**.
>
> Modern development operations face 'cloud blindness,' often overspending on forgotten or idle virtual instances. Our project scope resolves this by constructing a full-stack microservices application that unifies cross-cloud data ingestion, normalizes mixed billing objects, and sets up automated real-time alerting channels to catch budget breaches instantly."*

### 2. Architecture & The Choice of MongoDB [0:45 - 1:45]
> *"Let's examine our local architecture now running inside Docker Compose.
>
> We chose a **MongoDB NoSQL Document Store** rather than a traditional relational SQL engine. Why? Because multi-cloud APIs return unstructured, evolving JSON records. While AWS yields granular unblended line items, GCP models utilize flat metrics tracking datasets. A relational SQL approach would necessitate complex database table migrations whenever a cloud provider modifies a reporting property. MongoDB stores these changing JSON files natively into a single, high-performance database collection.
>
> Our **FastAPI backend** queries this document pool asynchronously to calculate metric aggregations, feeding a responsive **React.js and Recharts canvas** that enables dynamic asset ledger filtering over port `3000`."*

### 3. Monitoring, Dual Cost Alerting, & Live Verification [1:45 - 3:00]
> *"To ensure automated budget control, we deployed **Prometheus and Alertmanager**.
>
