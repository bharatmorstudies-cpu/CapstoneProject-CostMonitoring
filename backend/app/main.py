from app.database import init_db, save_cost_records
from app.collectors.aws_client import AWSBillingClient
from app.collectors.azure_client import AzureBillingClient
from app.collectors.gcp_client import GCPBillingClient

def run_aggregation_pipeline():
    print("=== Launching Sprint 2 Data Aggregation Pipeline ===")
    
    # Step 1: Ensure database schema is provisioned inside Docker
    init_db()
    
    # Step 2: Instantiate multi-cloud fetching agents
    aws = AWSBillingClient()
    azure = AzureBillingClient()
    gcp = GCPBillingClient()
    
    # Step 3: Fetch historical multi-cloud metrics
    all_extracted_records = []
    
    print("Aggregating cost logs from AWS...")
    # AWS client handles empty environments gracefully via try/except blocks
    all_extracted_records.extend(aws.fetch_historical_costs(days_back=7))
    
    print("Aggregating cost logs from Azure...")
    all_extracted_records.extend(azure.fetch_historical_costs(days_back=7))
    
    print("Aggregating cost logs from GCP...")
    all_extracted_records.extend(gcp.fetch_historical_costs(days_back=7))
    
    print(f"\nTotal multi-cloud logs collected: {len(all_extracted_records)}")
    
    # Step 4: Persist records into storage
    if all_extracted_records:
        save_cost_records(all_extracted_records)
    else:
        print("No active cost data collected to save.")

if __name__ == '__main__':
    run_aggregation_pipeline()
