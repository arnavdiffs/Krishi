from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TowerBase(BaseModel):
    name: str
    code: str
    latitude: float
    longitude: float
    radius_km: float = 10.0
    state: str
    district: str
    is_active: bool = True

class TowerCreate(TowerBase):
    pass

class Tower(TowerBase):
    id: int
    created_at: str

class FarmerBase(BaseModel):
    name: str
    phone: str
    village: str
    latitude: float
    longitude: float
    crop: str
    crop_stage: str
    language: str = "hi"  # hi, mr, pa, en
    opt_in_status: bool = True

class FarmerCreate(FarmerBase):
    pass

class Farmer(FarmerBase):
    id: int
    primary_tower_id: Optional[int] = None
    distance_to_tower_km: Optional[float] = None
    created_at: str

class StormEventRequest(BaseModel):
    tower_id: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rain_intensity_mm: float = Field(default=25.0, description="Precipitation in mm/hr")
    storm_radius_km: float = Field(default=10.0, description="Storm cloud radius")
    severity: str = Field(default="severe", description="moderate, severe, hail, cloudburst")
    notes: Optional[str] = "Sudden localized thunderstorm detected on radar"

class AlertDeliveryItem(BaseModel):
    farmer_id: int
    farmer_name: str
    phone: str
    crop: str
    crop_stage: str
    channel: str  # FLASH_SMS_CLASS_0, VOICE_CALL_IVR
    message: str
    urgency: str
    distance_km: float
    status: str

class AlertSummary(BaseModel):
    alert_id: int
    timestamp: str
    tower_id: Optional[int]
    tower_name: Optional[str]
    rain_intensity_mm: float
    severity: str
    description: str
    total_eligible_farmers: int
    high_risk_farmers_alerted: int
    moderate_risk_farmers_alerted: int
    deliveries: List[AlertDeliveryItem] = []
