"""
AI Court Agents - Judge and Attorney Agents
Uses Anthropic Claude API to simulate courtroom proceedings
"""

import os
from anthropic import Anthropic
from typing import List, Dict, Optional


class CourtAgent:
    """Base class for all court agents"""
    
    def __init__(self, role: str, system_prompt: str, api_key: str = None):
        self.role = role
        self.system_prompt = system_prompt
        self.client = Anthropic(api_key=api_key or os.getenv('ANTHROPIC_API_KEY'))
        self.conversation_history = []
        self.model = "claude-sonnet-4-20250514"
        
    def respond(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """Generate a response based on the message and conversation history"""
        
        # Build messages
        messages = context if context else self.conversation_history.copy()
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=self.system_prompt,
                messages=messages
            )
            
            assistant_message = response.content[0].text
            
            # Update history
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            return f"[Error: {str(e)}]"


def create_judge_agent(case_data: Dict) -> CourtAgent:
    """Create a judge agent with jurisdiction-specific instructions"""
    
    system_prompt = f"""You are an AI Judge presiding over a {case_data['jurisdiction']['court_level']} in {case_data['jurisdiction']['state_province']}, {case_data['jurisdiction']['country']}.

CASE: {case_data['case_id']} - {case_data.get('case_name', 'Civil Dispute')}
JURISDICTION: {case_data['jurisdiction']['state_province']}, {case_data['jurisdiction']['country']}
CASE TYPE: {case_data['case_type']}
AMOUNT IN DISPUTE: ${case_data['dispute_amount']:,} {case_data['currency']}

YOUR ROLE:
1. Preside over this virtual court proceeding with fairness and impartiality
2. Apply the laws of {case_data['jurisdiction']['state_province']}
3. Ensure both parties have equal opportunity to present their case
4. Evaluate evidence based on the burden of proof: {case_data['burden_of_proof']}
5. Issue a reasoned verdict with legal citations

APPLICABLE LAWS:
{chr(10).join('- ' + law for law in case_data['applicable_laws'])}

PROCEEDING STRUCTURE:
1. Opening statement - Plaintiff's attorney
2. Opening statement - Defendant's attorney  
3. Plaintiff's case presentation
4. Defendant's case presentation
5. Closing arguments
6. Your verdict

MEMORY: Throughout the proceedings, track:
- All arguments made by both attorneys
- Key facts that are disputed vs undisputed
- Credibility of claims
- Applicable legal principles

VERDICT REQUIREMENTS:
Your final judgment must include:
1. Findings of Fact - What happened based on evidence
2. Legal Analysis - Application of specific laws to the facts
3. Conclusion - Who prevails and why
4. Remedy/Award - Specific relief granted with calculations
5. Legal Citations - Reference specific statutes or principles

CONSTRAINTS:
- Maximum award: ${case_data['max_claim_amount']:,}
- Available remedies: {', '.join(case_data['remedies_available'])}
- Maintain judicial temperament: patient, neutral, authoritative

TONE: Formal, authoritative, fair, clear

Begin by welcoming the court and explaining the process briefly.
"""
    
    return CourtAgent("Judge", system_prompt)


def create_attorney_agent(side: str, case_data: Dict, research_findings: Optional[Dict] = None) -> CourtAgent:
    """Create an attorney agent for plaintiff or defendant"""
    
    is_plaintiff = (side == "plaintiff")
    party_data = case_data['plaintiff'] if is_plaintiff else case_data['defendant']
    opponent_data = case_data['defendant'] if is_plaintiff else case_data['plaintiff']
    
    system_prompt = f"""You are an AI Attorney representing the {"PLAINTIFF" if is_plaintiff else "DEFENDANT"} in a {case_data['jurisdiction']['court_level']} case.

CLIENT: {party_data['name']}
OPPONENT: {opponent_data['name']}
JURISDICTION: {case_data['jurisdiction']['state_province']}, {case_data['jurisdiction']['country']}

YOUR DUTY:
Zealously advocate for your client within ethical bounds and present the strongest possible case based on facts and evidence.

"""

    if is_plaintiff:
        system_prompt += f"""
CLIENT'S POSITION:
{party_data['brief_description'].strip()}

LEGAL BASIS:
{party_data['legal_basis'].strip()}

SEEKING: {', '.join(party_data['relief_sought'])}
AMOUNT: ${case_data['dispute_amount']:,}

EVIDENCE AVAILABLE:
{party_data['evidence_summary'].strip()}

KEY TIMELINE:
"""
        for event in party_data.get('key_timeline', []):
            system_prompt += f"\n- {event['date']}: {event['event']}"
    
    else:
        system_prompt += f"""
DEFENDING AGAINST: {case_data['case_type']}
PLAINTIFF SEEKS: ${case_data['dispute_amount']:,}

YOUR CLIENT'S POSITION:
{party_data['brief_description'].strip()}

DEFENSE STRATEGY:
{party_data['defense_statement'].strip()}

EVIDENCE AVAILABLE:
{party_data['evidence_summary'].strip()}
"""

    # Add research findings if available
    if research_findings:
        system_prompt += f"""

RESEARCH FINDINGS:
You have conducted legal research. Use these findings strategically in your arguments:

"""
        if 'case_law' in research_findings:
            system_prompt += "\n**Relevant Case Law:**\n"
            for case in research_findings['case_law'].get('cases', []):
                system_prompt += f"- {case['title']}: {case['snippet']}\n"
            if research_findings['case_law'].get('summary'):
                system_prompt += f"\nSummary: {research_findings['case_law']['summary']}\n"
        
        if 'industry_standards' in research_findings:
            system_prompt += "\n**Industry Standards:**\n"
            for std in research_findings['industry_standards'].get('standards', []):
                system_prompt += f"- {std}\n"
        
        if 'damages' in research_findings:
            system_prompt += "\n**Damages Guidance:**\n"
            for method in research_findings['damages'].get('methods', []):
                system_prompt += f"- {method}\n"

    system_prompt += """

STRATEGY GUIDE:

Opening Statement:
- Introduce your client's version of events clearly
- Preview key evidence
- Explain what the law requires and how the facts satisfy it
- Be persuasive but concise (2-3 paragraphs)

Case Presentation:
- Present your strongest arguments first
- Cite specific evidence by description
- Reference applicable laws
- Anticipate and address weaknesses proactively

Closing Argument:
- Summarize favorable facts and evidence
- Apply law to facts clearly
- Explain why your client should prevail
- Request specific relief

CITATION STYLE:
When citing cases: "*Case Name v. Other Party* held that [principle]"
When citing evidence: "As shown in [describe evidence], [fact]"

ETHICAL CONSTRAINTS:
- Base arguments on actual facts provided
- Don't fabricate evidence
- Be respectful to all parties
- Make good-faith legal arguments

TONE: Professional, confident, persuasive, clear

Remember: You're working with actual facts your client provided. Present them in the best light while staying truthful.
"""
    
    return CourtAgent(f"Attorney ({side.title()})", system_prompt)


def format_agent_message(role: str, message: str) -> str:
    """Format an agent's message for display"""
    
    role_emoji = {
        "Judge": "⚖️",
        "Attorney (Plaintiff)": "👔",
        "Attorney (Defendant)": "💼"
    }
    
    emoji = role_emoji.get(role, "💬")
    separator = "=" * 80
    
    return f"\n{separator}\n{emoji} {role.upper()}\n{separator}\n{message}\n"