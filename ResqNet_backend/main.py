from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ResQNet+ Insurance Decision Engine",
    description="Backend API for intelligent insurance policy recommendations and hospital network checks.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS – allow all origins so the frontend can connect freely
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class UninsuredProfile(BaseModel):
    """Profile data submitted by an uninsured user seeking policy recommendations."""
    age: int
    budget: int
    condition: str


class InsuredProfile(BaseModel):
    """Profile data submitted by an insured user to check their hospital network."""
    provider: str
    city: str


# ---------------------------------------------------------------------------
# Response type aliases (for clarity in return annotations)
# ---------------------------------------------------------------------------

Policy = dict
Hospital = dict

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def root():
    """Health-check endpoint."""
    return {"status": "ok", "service": "ResQNet+ Insurance Decision Engine"}


@app.post("/api/recommend-policy", tags=["Policy"])
def recommend_policy(profile: UninsuredProfile) -> List[Policy]:
    """
    Accept an UninsuredProfile and return a list of 3 recommended insurance policies.

    In production this would call the AI reasoning engine; for now it returns
    hardcoded demonstration data.
    """
    policies: List[Policy] = [
        {
            "id": "POL-001",
            "name": "ResQNet Shield Basic",
            "provider": "Star Health Insurance",
            "sum_insured": 500000,
            "room_rent": "1% of Sum Insured per day",
            "ped_waiting": "2 years",
            "price": 6800,
            "ai_reasoning": (
                f"Based on your age ({profile.age}) and budget (Rs.{profile.budget}), "
                "this entry-level plan offers solid hospitalisation cover with a short "
                "PED waiting period — ideal for first-time buyers with a pre-existing "
                f"condition like '{profile.condition}'."
            ),
        },
        {
            "id": "POL-002",
            "name": "ResQNet Care Plus",
            "provider": "HDFC ERGO Health",
            "sum_insured": 1000000,
            "room_rent": "Single private AC room",
            "ped_waiting": "3 years",
            "price": 11200,
            "ai_reasoning": (
                f"For a {profile.age}-year-old with '{profile.condition}', this mid-tier "
                "plan doubles the sum insured and includes a no-claim bonus of up to 50%. "
                "It fits within your declared budget and provides OPD cover from day one."
            ),
        },
        {
            "id": "POL-003",
            "name": "ResQNet Elite 360",
            "provider": "Niva Bupa Health Insurance",
            "sum_insured": 2000000,
            "room_rent": "No room-rent sub-limit",
            "ped_waiting": "1 year (with declaration)",
            "price": 18500,
            "ai_reasoning": (
                f"If your budget can stretch, this premium plan is the strongest match "
                f"for age {profile.age} with '{profile.condition}'. It offers worldwide "
                "emergency cover, mental health benefits, and a reduced PED waiting period "
                "of only 1 year upon medical declaration."
            ),
        },
    ]
    return policies


@app.post("/api/check-network", tags=["Network"])
def check_network(profile: InsuredProfile) -> List[Hospital]:
    """
    Accept an InsuredProfile and return a list of 3 nearby cashless hospitals.

    In production this would query a live hospital-network database; for now
    it returns hardcoded demonstration data.
    """
    hospitals: List[Hospital] = [
        {
            "name": f"City Care Hospital – {profile.city}",
            "distance": "1.2 km",
            "is_cashless": True,
        },
        {
            "name": f"Apollo Spectra – {profile.city} Central",
            "distance": "3.5 km",
            "is_cashless": True,
        },
        {
            "name": f"Sunrise Medical Centre – {profile.city}",
            "distance": "5.8 km",
            "is_cashless": False,
        },
    ]
    return hospitals
