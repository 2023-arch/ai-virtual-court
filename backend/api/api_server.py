from __future__ import annotations

import uuid
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException

from backend.court_agents import CourtAgentError
from pydantic import BaseModel, Field

from backend.full_agents import FullCourtSystem


class TimelineEvent(BaseModel):
    date: str
    event: str


class PartyData(BaseModel):
    name: str
    brief_description: str
    evidence_summary: str
    legal_basis: Optional[str] = ""
    defense_statement: Optional[str] = ""
    relief_sought: List[str] = Field(default_factory=list)
    key_timeline: List[TimelineEvent] = Field(default_factory=list)


class Jurisdiction(BaseModel):
    court_level: str
    state_province: str
    country: str


class CaseData(BaseModel):
    case_id: str
    case_name: str = "Civil Dispute"
    case_type: str
    currency: str = "USD"
    dispute_amount: int
    max_claim_amount: int
    burden_of_proof: str
    applicable_laws: List[str]
    remedies_available: List[str]
    jurisdiction: Jurisdiction
    plaintiff: PartyData
    defendant: PartyData


class StartTrialRequest(BaseModel):
    case_data: CaseData
    enable_research: bool = False


class TrialStepRequest(BaseModel):
    trial_id: str


class TrialResponse(BaseModel):
    trial_id: str
    case_id: str
    complete: bool
    transcript: List[Dict[str, str]]


app = FastAPI(title="AI Virtual Court API", version="0.1.0")

TRIALS: Dict[str, Dict] = {}


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/trial/start", response_model=TrialResponse)
def start_trial(req: StartTrialRequest) -> TrialResponse:
    try:
        system = FullCourtSystem(req.case_data.model_dump(), enable_research=req.enable_research)
        state = system.start_trial()
    except CourtAgentError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    trial_id = str(uuid.uuid4())
    TRIALS[trial_id] = {"system": system, "state": state}

    return TrialResponse(
        trial_id=trial_id,
        case_id=state.case_id,
        complete=state.complete,
        transcript=state.transcript,
    )


@app.post("/trial/step", response_model=TrialResponse)
def trial_step(req: TrialStepRequest) -> TrialResponse:
    trial = TRIALS.get(req.trial_id)
    if not trial:
        raise HTTPException(status_code=404, detail="trial_id not found")

    state = trial["system"].advance_trial(trial["state"])
    trial["state"] = state

    return TrialResponse(
        trial_id=req.trial_id,
        case_id=state.case_id,
        complete=state.complete,
        transcript=state.transcript,
    )
