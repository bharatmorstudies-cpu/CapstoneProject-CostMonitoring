import os
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.mgmt.costmanagement import CostManagementClient
from azure.mgmt.costmanagement.models import QueryDefinition, QueryTimePeriod, QueryDataset, QueryAggregation, QueryGrouping

class AzureBillingClient:
    def __init__(self):
        tenant_id = os.getenv('AZURE_TENANT_ID')
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        
        # Safe initialization check to prevent SDK crashes on empty local environments
        if not all([tenant_id, client_id, client_secret]):
            print("Azure Credentials missing or incomplete. Using Local Simulation Mode.")
            self.client = None
        else:
            self.credential = ClientSecretCredential(
                tenant_id=tenant_id,
                client_id=client_id,
                client_secret=client_secret
            )
            self.client = CostManagementClient(self.credential)

    def fetch_historical_costs(self, days_back=7):
        """Queries Azure cost logs or safely falls back to local simulation tracking data."""
        if not self.client or not self.subscription_id:
            mock_records = []
            for i in range(days_back):
                target_date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
                mock_records.append({
                    "provider": "Azure",
                    "date": target_date,
                    "resource_type": "Virtual Machines",
                    "cost": 55.40 + (i * 2.10),
                    "environment": os.getenv('ENVIRONMENT', 'development')
                })
                mock_records.append({
                    "provider": "Azure",
                    "date": target_date,
                    "resource_type": "Azure SQL Database",
                    "cost": 28.50,
                    "environment": os.getenv('ENVIRONMENT', 'development')
                })
            return mock_records
            
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)
        scope = f"/subscriptions/{self.subscription_id}"
        
        query = QueryDefinition(
            type="ActualCost",
            timeframe="Custom",
            time_period=QueryTimePeriod(from_property=start_date, to=end_date),
            dataset=QueryDataset(
                granularity="Daily",
                aggregation={"PreTaxCost": QueryAggregation(name="PreTaxCost", function="Sum")},
                grouping=[QueryGrouping(type="Dimension", name="ResourceType")]
            )
        )
        
        try:
            response = self.client.query.usage(scope, query)
            standardized_records = []
            if response and response.rows:
                for row in response.rows:
                    cost_amount = float(row[0])
                    date_int = str(row[1])
                    parsed_date = datetime.strptime(date_int, "%Y%m%d").strftime("%Y-%m-%d")
                    resource_type = row[2] if row[2] else "Unknown"
                    
                    if cost_amount > 0:
                        standardized_records.append({
                            "provider": "Azure",
                            "date": parsed_date,
                            "resource_type": resource_type,
                            "cost": cost_amount,
                            "environment": os.getenv('ENVIRONMENT', 'development')
                        })
            return standardized_records
        except Exception as e:
            print(f"Error fetching Azure costs: {str(e)}")
            return []
