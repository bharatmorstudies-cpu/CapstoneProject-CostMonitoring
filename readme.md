Complete Sprint-by-Sprint Project Execution Plan
🛠️ Sprint 1: Project Setup and Basic Cloud Integration
Goal: Establish cloud provider connectivity and fetch baseline sample payloads to lay the development groundwork 
Execution Tasks:Repository
Build: Create a clean repository structure containing dedicated /backend and /frontend folders .Environment 
Isolation: Set up local .env configuration files to securely manage credentials for AWS, Azure, and GCP 
Connectivity Verification: Write script connectors leveraging boto3, azure-mgmt-costmanagement, and google-cloud-billing SDKs to verify infrastructure permissions 
Data Shape Analysis: Pull real metadata records from cloud endpoints and analyze their underlying JSON models 
![Multi-Cloud CostOps Dashboard Architecture](./Snapshots/Architecture.png)

# Capstone-CostMonitoring: Multi-Cloud DevOps Cost Dashboard

Centralized enterprise cloud tool designed to aggregate resource configurations and multi-cloud expenditure records cleanly across AWS, Azure, and GCP tracking boundaries.

## Architectural Sprint Status Tracker
- [x] **Sprint 1**: Connect Cloud Provider APIs and verify integration data structures.
- [x] **Sprint 2**: Stand up PostgreSQL persistence schema and configure cron synchronization engines.
- [ ] **Sprint 3**: Real-Time REST APIs and core UI dashboard deployment.
- [ ] **Sprint 4**: Time-series analytics trend calculations and charting.
- [ ] **Sprint 5**: Alertmanager implementation and communication webhooks.
- [ ] **Sprint 6**: Production Docker orchestration and optimization audit setups.

## Local Installation / Testing Run Guide (Sprints 1 & 2)

### Phase 1: Boot Up the PostgreSQL Service Infrastructure
Navigate to the root level project directory: `C:\Users\nagin\Documents\Capstone-CostMonitoring\`
```powershell
# Launch the persistent data storage layer inside Docker
docker-compose up -d
```

### Phase 2: Run the Pipeline Synchronization Script
Navigate into the backend folder directory:
```powershell
cd backend

# Windows PowerShell execution policy verification bypass parameters
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\venv\Scripts\Activate.ps1

# Execute dependencies install
python -m pip install -r requirements.txt

# Run the data aggregation pipeline engine
python -m app.main
```
