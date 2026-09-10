from typing import List
from app.core.schemas import EquipmentItem

EQUIPMENT_REGISTRY: List[EquipmentItem] = [
    EquipmentItem(
        equipment_id="EQ_IT_01",
        equipment_name="Server Rack",
        load_tier="Critical",
        rated_power_kw=3.5,
        location="IT Data Room",
        schedule_description="24/7 Continuous Operation",
        is_essential=True,
        channel_key="it_network_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_IT_02",
        equipment_name="WiFi / Network Switches",
        load_tier="Critical",
        rated_power_kw=1.5,
        location="Campus Admin",
        schedule_description="24/7 Continuous Operation",
        is_essential=True,
        channel_key="it_network_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_LT_01",
        equipment_name="Main Security & Corridor Lighting",
        load_tier="Essential",
        rated_power_kw=8.0,
        location="Campus Grounds",
        schedule_description="Nightly (6 PM - 6 AM)",
        is_essential=True,
        channel_key="lighting_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_WP_01",
        equipment_name="Overhead Tank Water Pump",
        load_tier="Essential",
        rated_power_kw=7.5,
        location="Pump Station",
        schedule_description="Flexible (Originally 5 PM - 7 PM)",
        is_essential=True,
        channel_key="water_pump_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_KT_01",
        equipment_name="Kitchen Cooking & Refrigeration",
        load_tier="Essential",
        rated_power_kw=10.0,
        location="Mess Hall",
        schedule_description="Meal Times (6 AM - 9 PM)",
        is_essential=True,
        channel_key="kitchen_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_HVAC_01",
        equipment_name="Academic Block HVAC Chillers",
        load_tier="Flexible",
        rated_power_kw=25.0,
        location="Academic Blocks",
        schedule_description="Working Hours (8 AM - 6 PM)",
        is_essential=False,
        channel_key="hvac_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_LT_02",
        equipment_name="Classroom & Lab Lighting",
        load_tier="Flexible",
        rated_power_kw=6.0,
        location="Classrooms A-D",
        schedule_description="Class Hours (8 AM - 5 PM)",
        is_essential=False,
        channel_key="lighting_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_LAB_01",
        equipment_name="Heavy CNC Machine",
        load_tier="Flexible",
        rated_power_kw=12.0,
        location="Workshop",
        schedule_description="Shift Hours (originally peak tariff 2 PM - 5 PM)",
        is_essential=False,
        channel_key="lab_equipment_kw"
    ),
    EquipmentItem(
        equipment_id="EQ_LAB_02",
        equipment_name="3D Printers & PCB Mill",
        load_tier="Flexible",
        rated_power_kw=4.0,
        location="Innovation Lab",
        schedule_description="Lab Hours (10 AM - 4 PM)",
        is_essential=False,
        channel_key="lab_equipment_kw"
    ),
]

def get_equipment_by_id(equipment_id: str) -> EquipmentItem:
    for eq in EQUIPMENT_REGISTRY:
        if eq.equipment_id == equipment_id:
            return eq
    raise ValueError(f"Equipment with ID {equipment_id} not found.")

def get_all_equipment() -> List[EquipmentItem]:
    return EQUIPMENT_REGISTRY
