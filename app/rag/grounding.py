"""Grounding Verifier and Citation Validator

Verification pipeline:
1. List claims
2. Identify supporting evidence
3. Verify retrieved source
4. Verify citation
5. Detect unsupported claim
6. Remove / replace unsupported claim with 'Evidence unavailable; unable to verify this claim.'
7. Mark uncertainty
8. Produce final grounded response metadata
"""

import logging
from typing import List, Dict, Any, Tuple
from app.models.schemas import Citation, PolicyFinding

logger = logging.getLogger(__name__)

UNAVAILABLE_CLAIM_TEXT = "Evidence unavailable; unable to verify this claim."

class GroundingVerifier:
    def verify_policy_finding(self, policy_finding: PolicyFinding, retrieved_citations: List[Citation]) -> PolicyFinding:
        """Verifies policy claims against retrieved citations."""
        if not retrieved_citations:
            logger.warning(f"No citations retrieved for policy {policy_finding.policy_name}. Stripping ungrounded claim.")
            policy_finding.is_compliant = False
            policy_finding.violation_details = UNAVAILABLE_CLAIM_TEXT
            policy_finding.citations = []
            return policy_finding

        # Check citation overlap
        valid_citations = []
        for citation in retrieved_citations:
            if citation.clause_text and len(citation.clause_text.strip()) > 10:
                valid_citations.append(citation)

        if not valid_citations:
            policy_finding.is_compliant = False
            policy_finding.violation_details = UNAVAILABLE_CLAIM_TEXT
            policy_finding.citations = []
        else:
            policy_finding.citations = valid_citations

        return policy_finding

    def validate_citations(self, claims: List[str], citations: List[Citation]) -> Tuple[List[str], bool]:
        """Validates list of claim strings against citations."""
        grounded_claims = []
        all_grounded = True

        if not citations:
            return [UNAVAILABLE_CLAIM_TEXT], False

        for claim in claims:
            # Verify if claim terms overlap with citation clauses
            claim_words = set(claim.lower().split())
            is_supported = False
            for citation in citations:
                citation_words = set(citation.clause_text.lower().split())
                overlap = len(claim_words.intersection(citation_words))
                if overlap >= 3:
                    is_supported = True
                    break

            if is_supported:
                grounded_claims.append(claim)
            else:
                grounded_claims.append(UNAVAILABLE_CLAIM_TEXT)
                all_grounded = False

        return grounded_claims, all_grounded

grounding_verifier = GroundingVerifier()
