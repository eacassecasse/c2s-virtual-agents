"""
MCP Client Tools for AI Agent
"""
import requests
from typing import Optional, Dict, List
from langchain.tools import tool
from pydantic import Field

MCP_SERVER_URL = "http://localhost:8000/mcp/query"


class MCPClient:
    @staticmethod
    def _send_request(operation: str, model: str, filters: Optional[Dict] = None, limit: Optional[int] = None):
        payload = {
            "operation": operation,
            "model": model,
            "filters": filters or {},
            "limit": limit
        }
        response = requests.post(MCP_SERVER_URL, json=payload)
        return response.json()

    @tool()
    def list_vehicles(limit: int = 5) -> str:
        """List vehicles from MCP server"""
        response = MCPClient._send_request("list", "vehicle", limit=limit)
        if not response['success']:
            return f"Error: {response['error']}"
        return _format_vehicles(response['data'])

    @tool()
    def filter_vehicles(
            color: Optional[str] = Field(None, description="Vehicle color filter"),
            year: Optional[int] = Field(None, description="Manufacture year filter"),
            brand: Optional[str] = Field(None, description="Brand name filter"),
            model: Optional[str] = Field(None, description="Model name filter")
    ) -> str:
        """Filter vehicles through MCP server"""
        filters = {k: v for k, v in locals().items() if v is not None}
        if color:
            filters['color'] = color

        if year:
            filters['year_of_manufacture'] = year

        if brand:
            filters['brand_name'] = brand
        if model:
            filters['model_name'] = model

        response = MCPClient._send_request("filter", "vehicle", filters=filters)
        if not response['success']:
            return f"Error: {response['error']}"
        return _format_vehicles(response['data'])


def _format_vehicles(vehicles: List[Dict]) -> str:
    """Format vehicle data for LLM consumption"""
    if not vehicles:
        return "No vehicles found"

    return "\n\n".join(
        f"ID: {v['id']}\n"
        f"Brand: {v.get('brand_name', 'N/A')}\n"
        f"Model: {v.get('model_name', 'N/A')}\n"
        f"Color: {v['color']}\n"
        f"Year: {v['year_of_manufacture']}\n"
        f"Plate: {v['license_plate']}"
        for v in vehicles
    )
