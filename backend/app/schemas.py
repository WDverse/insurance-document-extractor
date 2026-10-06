"""Data models shared by the pipeline, the API and the LLM structured output."""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    policy = "policy"
    application = "application"
    other = "other"


class Beneficiary(BaseModel):
    name: str = Field(description="Full name of the beneficiary")
    relationship: Optional[str] = Field(None, description="Relationship to the insured, e.g. spouse, child")
    percentage: Optional[float] = Field(None, description="Share of the benefit as a percentage (0-100)")


class PolicyFields(BaseModel):
    """Structured fields pulled from an insurance policy or application."""

    document_type: DocumentType = Field(DocumentType.other, description="policy, application, or other")
    policy_number: Optional[str] = Field(None, description="Policy or application reference number")
    product: Optional[str] = Field(None, description="Product name, e.g. Term Life 20, Critical Illness")
    insured_name: Optional[str] = Field(None, description="Full name of the insured person")
    date_of_birth: Optional[date] = Field(None, description="Insured's date of birth (YYYY-MM-DD)")
    coverage_amount: Optional[float] = Field(None, description="Death benefit / coverage amount in CAD, number only")
    premium_amount: Optional[float] = Field(None, description="Premium amount in CAD, number only")
    premium_frequency: Optional[str] = Field(None, description="monthly or annual")
    effective_date: Optional[date] = Field(None, description="Policy effective / start date (YYYY-MM-DD)")
    term_years: Optional[int] = Field(None, description="Length of the term in years, if a term product")
    beneficiaries: list[Beneficiary] = Field(default_factory=list, description="Named beneficiaries")


class Severity(str, Enum):
    error = "error"      # must be fixed before the document is usable
    warning = "warning"  # a human should double-check


class Issue(BaseModel):
    field: str
    severity: Severity
    message: str


REQUIRED_FIELDS = ["policy_number", "insured_name", "date_of_birth", "coverage_amount", "premium_amount"]
