SAMPLE_CASE = {
    "case_id": "AVC-2026-001",
    "case_name": "Acme Corp v. ByteWorks LLC",
    "case_type": "Breach of Contract",
    "currency": "USD",
    "dispute_amount": 85000,
    "max_claim_amount": 100000,
    "burden_of_proof": "Preponderance of the evidence",
    "applicable_laws": [
        "State contract law",
        "Uniform Commercial Code principles where applicable",
        "Duty to mitigate damages",
    ],
    "remedies_available": ["Compensatory damages", "Specific performance", "Declaratory relief"],
    "jurisdiction": {
        "court_level": "Superior Court",
        "state_province": "California",
        "country": "USA",
    },
    "plaintiff": {
        "name": "Acme Corp",
        "brief_description": "Acme hired ByteWorks to deliver a custom internal workflow system by May 1, 2025.",
        "legal_basis": "Defendant materially breached delivery and support obligations.",
        "evidence_summary": "Signed MSA/SOW, invoice records, email timeline, and failed QA reports.",
        "relief_sought": ["Compensatory damages", "Costs"],
        "key_timeline": [
            {"date": "2025-01-10", "event": "SOW executed"},
            {"date": "2025-05-01", "event": "Delivery deadline missed"},
            {"date": "2025-06-01", "event": "Notice of breach sent"},
        ],
    },
    "defendant": {
        "name": "ByteWorks LLC",
        "brief_description": "ByteWorks claims Acme repeatedly changed scope and withheld required test data.",
        "defense_statement": "Any delays were excused by plaintiff-caused scope changes and dependency delays.",
        "evidence_summary": "Change request log, acceptance criteria revisions, project status emails.",
    },
}
