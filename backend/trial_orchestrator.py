from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from backend.court_agents import CourtAgent, format_agent_message


@dataclass
class TrialState:
    case_id: str
    transcript: List[Dict[str, str]] = field(default_factory=list)
    stage_index: int = 0
    complete: bool = False


class TrialOrchestrator:
    STAGES = [
        ("Attorney (Plaintiff)", "Deliver your opening statement."),
        ("Attorney (Defendant)", "Deliver your opening statement."),
        ("Attorney (Plaintiff)", "Present your full case with key evidence."),
        ("Attorney (Defendant)", "Present your full defense with key evidence."),
        ("Attorney (Plaintiff)", "Deliver your closing argument."),
        ("Attorney (Defendant)", "Deliver your closing argument."),
        ("Judge", "Issue your verdict and reasoning."),
    ]

    def __init__(self, judge: CourtAgent, plaintiff: CourtAgent, defendant: CourtAgent):
        self.agents = {
            "Judge": judge,
            "Attorney (Plaintiff)": plaintiff,
            "Attorney (Defendant)": defendant,
        }

    def start(self, case_data: Dict) -> TrialState:
        state = TrialState(case_id=case_data["case_id"])
        intro = self.agents["Judge"].respond("Open the court proceedings now.")
        state.transcript.append({"role": "Judge", "message": intro})
        return state

    def step(self, state: TrialState) -> TrialState:
        if state.complete:
            return state

        role, instruction = self.STAGES[state.stage_index]
        message = self.agents[role].respond(instruction)
        state.transcript.append({"role": role, "message": message})

        state.stage_index += 1
        if state.stage_index >= len(self.STAGES):
            state.complete = True

        return state

    @staticmethod
    def render_transcript(state: TrialState) -> str:
        return "\n".join(
            format_agent_message(item["role"], item["message"]) for item in state.transcript
        )
