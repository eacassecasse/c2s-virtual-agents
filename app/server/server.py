#!/usr/bin/python3
"""
Defines the Model Context Protocol server
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from app.models import storage
from app.models.vehicle import Vehicle
from app.models.vehicle_model import VehicleModel
from app.models.brand import Brand

app = FastAPI()


class MCPRequest(BaseModel):
    operation: str
    model: str
    filters: Optional[Dict] = None
    limit: Optional[int] = None


class MCPResponse(BaseModel):
    success: bool
    data: Optional[List[Dict]] = None
    error: Optional[str] = None


def get_related_names(vehicle_dict: Dict) -> Dict:
    """Enhance vehicle data with related model info"""
    model = storage.get(VehicleModel, vehicle_dict['vehicle_model_id'])
    if model:
        vehicle_dict['model_name'] = model.name
        brand = storage.get(Brand, model.brand_id)
        if brand:
            vehicle_dict['brand_name'] = brand.name
    return vehicle_dict


@app.post("/mcp/query")
async def handle_mcp_request(request: MCPRequest) -> MCPResponse:
    try:
        if request.operation == "list":
            vehicles = list(storage.all(Vehicle).values())
            vehicles = [get_related_names(v.to_dict()) for v in vehicles[:request.limit or 5]]
            return MCPResponse(success=True, data=vehicles)

        elif request.operation == "filter":
            results = []
            for vehicle in storage.all(Vehicle).values():
                val = get_related_names(vehicle.to_dict())
                if all(
                        str(v.get(k, "")).lower() == str(v).lower()
                        for k, v in request.filters.items() if v is not None
                ):
                    results.append(val)
            return MCPResponse(success=True, data=results)

        else:
            return MCPResponse(success=False, error="Invalid operation")

    except Exception as e:
        return MCPResponse(success=False, error=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)