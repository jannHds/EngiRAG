
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class VisibilityScope(str, Enum):
    PRIVATE_CONVERSATION = "PRIVATE_CONVERSATION"
    SHARED = "SHARED"


class ValidationStatus(str, Enum):
    PENDING = "PENDING"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class EvidenceType(str, Enum):
    TEXT = "TEXT"
    TABLE = "TABLE"
    FIGURE = "FIGURE"
    OTHER = "OTHER"


class RetrievalMode(str, Enum):
    DENSE = "dense"
    LEXICAL = "lexical"
    HYBRID = "hybrid"


class QueryLanguage(str, Enum):
    AUTO = "auto"
    AR = "ar"
    EN = "en"


class DocumentReference(StrictModel):
    document_id: UUID
    document_version_id: UUID
    visibility_scope: VisibilityScope
    owner_id: int | None = Field(default=None, gt=0)
    conversation_id: UUID | None = None

    @model_validator(mode="after")
    def validate_scope(self):
        if self.visibility_scope == VisibilityScope.PRIVATE_CONVERSATION:
            if self.owner_id is None or self.conversation_id is None:
                raise ValueError(
                    "Private documents require an owner and conversation."
                )

        if self.visibility_scope == VisibilityScope.SHARED:
            if self.owner_id is not None or self.conversation_id is not None:
                raise ValueError(
                    "Shared documents cannot have private ownership fields."
                )

        return self


class EngineeringFact(StrictModel):
    equipment_identifier: str | None = None
    parameter_name: str = Field(min_length=1)
    value_text: str = Field(min_length=1)
    unit: str | None = None
    header_hierarchy: list[str] = Field(default_factory=list)
    source_cell_range: str | None = None


class SourceLocation(StrictModel):
    pdf_page_index: int | None = Field(default=None, ge=0)
    printed_page_label: str | None = None
    section_reference: str | None = None
    table_reference: str | None = None
    row_reference: str | None = None
    column_reference: str | None = None
    cell_range: str | None = None
    heading_hierarchy: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def require_location(self):
        if not any([
            self.pdf_page_index is not None,
            self.printed_page_label,
            self.section_reference,
            self.table_reference,
            self.cell_range,
        ]):
            raise ValueError("At least one source locator is required.")
        return self


class EvidenceRecord(StrictModel):
    evidence_id: UUID
    source: DocumentReference
    content_revision_id: UUID
    content: str = Field(min_length=1)

    # Legacy fields retained for existing integration tests.
    page_number: int | None = Field(default=None, ge=1)
    section_reference: str | None = None

    evidence_type: EvidenceType = EvidenceType.TEXT
    language: str | None = None
    heading_hierarchy: list[str] = Field(default_factory=list)

    engineering_facts: list[EngineeringFact] = Field(
        default_factory=list
    )
    source_locations: list[SourceLocation] = Field(
        default_factory=list
    )

    extraction_method: str | None = None
    extraction_confidence: float | None = Field(
        default=None, ge=0, le=1
    )
    extraction_issue_location: str | None = None

    validation_status: ValidationStatus = ValidationStatus.PENDING
    previous_evidence_id: UUID | None = None

    @model_validator(mode="after")
    def check_approved_evidence(self):
        if self.validation_status == ValidationStatus.APPROVED:
            if not (
                self.source_locations
                or self.page_number is not None
                or self.section_reference
            ):
                raise ValueError(
                    "Approved evidence requires a source location."
                )
        return self


class AuthorizedRetrievalRequest(StrictModel):
    question: str = Field(min_length=1)
    requester_user_id: int = Field(gt=0)
    conversation_id: UUID
    authorized_document_version_ids: list[UUID] = Field(
        default_factory=list
    )
    top_k: int = Field(default=5, ge=1, le=20)

    query_language: QueryLanguage = QueryLanguage.AUTO
    retrieval_mode: RetrievalMode = RetrievalMode.DENSE

    # These settings must be selected by trusted backend logic.
    index_generation_id: UUID | None = None
    retrieval_profile_id: UUID | None = None


class RetrievalScores(StrictModel):
    dense_score: float | None = None
    lexical_score: float | None = None
    fusion_score: float | None = None


class RetrievedChunk(StrictModel):
    chunk_id: UUID
    chunk_text: str = Field(min_length=1)
    index_generation_id: UUID
    document_title: str = Field(min_length=1)

    rank: int = Field(ge=1)
    retrieval_method: RetrievalMode
    scores: RetrievalScores

    evidence_records: list[EvidenceRecord] = Field(min_length=1)

    @model_validator(mode="after")
    def check_retrieved_evidence(self):
        first = self.evidence_records[0]

        for evidence in self.evidence_records:
            if evidence.validation_status != ValidationStatus.APPROVED:
                raise ValueError(
                    "Retrieved evidence must be approved."
                )

            if (
                evidence.source.document_version_id
                != first.source.document_version_id
                or evidence.content_revision_id
                != first.content_revision_id
                or evidence.source.visibility_scope
                != first.source.visibility_scope
                or evidence.source.document_id
                != first.source.document_id
                or evidence.source.owner_id
                != first.source.owner_id
                or evidence.source.conversation_id
                != first.source.conversation_id
            ):
                raise ValueError(
                    "A chunk cannot mix different document, revision, "
                    "or access scopes."
                )

        return self
