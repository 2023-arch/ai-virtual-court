from __future__ import annotations

import os
from typing import Dict


class TavilyResearcher:
    """Minimal research adapter.

    If TAVILY_API_KEY is missing, returns deterministic fallback notes.
    """

    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")

    def research_for_side(self, case_data: Dict, side: str) -> Dict:
        case_type = case_data.get("case_type", "civil dispute")
        if not self.api_key:
            return {
                "case_law": {
                    "cases": [
                        {
                            "title": f"Sample precedent for {case_type}",
                            "snippet": "Courts evaluate contractual duty, breach, causation, and damages.",
                        }
                    ],
                    "summary": "Fallback research generated locally because TAVILY_API_KEY is not set.",
                },
                "industry_standards": {
                    "standards": [
                        "Document communication timelines and scope changes.",
                        "Use objective records for proving damages.",
                    ]
                },
                "damages": {
                    "methods": [
                        "Expectation damages",
                        "Reliance damages",
                        "Mitigation offset",
                    ]
                },
                "meta": {"side": side},
            }

        # Placeholder for real Tavily integration.
        return {
            "case_law": {"cases": [], "summary": "Live Tavily integration not yet implemented."},
            "industry_standards": {"standards": []},
            "damages": {"methods": []},
            "meta": {"side": side},
        }
