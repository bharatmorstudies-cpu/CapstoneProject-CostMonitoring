import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from motor.motor_asyncio import AsyncIOMotorClient
from prometheus_client import generate_latest, Gauge
from dotenv import load_dotenv

# Initialize project environmental context variables
load_dotenv()

app = FastAPI(title="Capstone Multi-Cloud Cost Analytics API Framework")

# Enable CORS so your React visual dashboard can safely read API telemetry records
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust with your explicit web domain url context when deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate a permanent Prometheus Gauge metric object inside memory storage context
# This maps directly to your custom condition constraint 'cloud_cost_daily_burn_rate > 100'
BURN_RATE_GAUGE = Gauge(
    'cloud_cost_daily_burn_rate', 
    'Aggregated active multi-cloud financial spend line items tracking parameter'
)

# Shared memory database contexts 
db_client = None
db = None

@app.on_event("startup")
async def startup_db_client():
    global db_client, db
    mongo_uri = os.getenv("MONGO_URI", "mongodb://root:SecureMongoPassword123@localhost:27017/devops_metrics?authSource=admin")
    try:
        # Utilizing Asynchronous non-blocking network connection pooling
        db_client = AsyncIOMotorClient(mongo_uri)
        db = db_client["devops_metrics"]
        print("✅ Asynchronous connection pooling established cleanly with MongoDB Cluster.")
    except Exception as e:
        print(f"❌ Core API Database startup context fault: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    global db_client
    if db_client:
        db_client.close()
        print("🔒 Database connections closed down safely.")

@app.get("/api/costs/summary")
async def get_cost_summary():
    """
    Dashboard Summary Endpoint.
    Aggregates metrics rows from database to process unified dashboards summary parameters.
    """
    if db is None:
        raise HTTPException(status_code=500, detail="Database context layer is inactive.")
        
    try:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "provider": "$provider",
                        "service": "$service"
                    },
                    "total_spending": {"$sum": "$cost"},
                    "currency": {"$first": "$currency"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "provider": "$_id.provider",
                    "service": "$_id.service",
                    "total_spending": {"$round": ["$total_spending", 2]},
                    "currency": 1
                }
            },
            {"$sort": {"total_spending": -1}}
        ]
        
        cursor = db["cloud_costs"].aggregate(pipeline)
        results = await cursor.to_list(length=100)
        return {"status": "success", "count": len(results), "data": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database aggregation exception: {str(e)}")

@app.get("/api/costs/timeline")
async def get_cost_timeline():
    """Queries and tracks chronological cross-cloud daily outlays trend models."""
    if db is None:
        raise HTTPException(status_code=500, detail="Database layer offline.")
    try:
        pipeline = [
            {
                "$group": {
                    "$group": {
                        "_id": "$date",
                        "AWS": {"$sum": {"$cond": [{"$eq": ["$provider", "AWS"]}, "$cost", 0]}},
                        "GCP": {"$sum": {"$cond": [{"$eq": ["$provider", "GCP"]}, "$cost", 0]}}
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "date": "$_id",
                    "AWS": {"$round": ["$AWS", 2]},
                    "GCP": {"$round": ["$GCP", 2]}
                }
            },
            {"$sort": {"date": 1}}
        ]
        cursor = db["cloud_costs"].aggregate(pipeline)
        results = await cursor.to_list(length=50)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """
    Prometheus Exporter Route.
    Queries MongoDB, updates the metric gauge, and outputs raw data streams for the scraper.
    """
    if db is None:
        return PlainTextResponse("Database disconnected", status_code=500)
        
    try:
        # Sum up all costs stored in our normalized data collection matrix
        cursor = db["cloud_costs"].find({})
        total_aggregated_spend = 0.0
        
        async for document in cursor:
            total_aggregated_spend += float(document.get("cost", 0.0))
            
        # Dynamically push the current database totals straight into the Prometheus tracking gauge
        BURN_RATE_GAUGE.set(total_aggregated_spend)
        
        return PlainTextResponse(generate_latest().decode("utf-8"))
    except Exception as e:
        return PlainTextResponse(f"Metrics collection error: {str(e)}", status_code=500)

@app.get("/api/health")
def api_health():
    return {"status": "healthy", "engine": "FastAPI Web Core"}
