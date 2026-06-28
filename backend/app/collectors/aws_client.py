import boto3
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class AWSBillingClient:
    def __init__(self):
        self.client = boto3.client(
            'ce',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )

    def fetch_historical_costs(self, days_back=7):
        """Fetches daily costs for the specified trailing window."""
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days_back)
        
        try:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'}
                ]
            )
            
            standardized_records = []
            for results in response.get('ResultsByTime', []):
                date_str = results['TimePeriod']['Start']
                for group in results.get('Groups', []):
                    service_name = group['Keys'][0]
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    
                    if amount > 0:
                        standardized_records.append({
                            "provider": "AWS",
                            "date": date_str,
                            "resource_type": service_name,
                            "cost": amount,
                            "environment": os.getenv('ENVIRONMENT', 'development')
                        })
            return standardized_records
        except Exception as e:
            print(f"Error fetching AWS costs: {str(e)}")
            return []
