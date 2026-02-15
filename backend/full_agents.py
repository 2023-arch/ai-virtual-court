from __future__ import annotations

from typing import Dict, Optional

from backend.court_agents import create_attorney_agent, create_judge_agent
from backend.tavily_researcher import TavilyResearcher
from backend.trial_orchestrator import TrialOrchestrator, TrialState


class FullCourtSystem:
    """Builds and runs the full AI-court flow."""

    def __init__(self, case_data: Dict, enable_research: bool = False):
        self.case_data = case_data
        researcher = TavilyResearcher() if enable_research else None

        plaintiff_research: Optional[Dict] = None
        defendant_research: Optional[Dict] = None

        if researcher:
            plaintiff_research = researcher.research_for_side(case_data, "plaintiff")
            defendant_research = researcher.research_for_side(case_data, "defendant")

        judge = create_judge_agent(case_data)
        plaintiff = create_attorney_agent(
            "plaintiff", case_data, research_findings=plaintiff_research
        )
        defendant = create_attorney_agent(
            "defendant", case_data, research_findings=defendant_research
        )

        self.orchestrator = TrialOrchestrator(judge, plaintiff, defendant)

    def start_trial(self) -> TrialState:
        return self.orchestrator.start(self.case_data)

    def advance_trial(self, state: TrialState) -> TrialState:
        return self.orchestrator.step(state)
