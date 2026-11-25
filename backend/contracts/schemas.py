
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class VisibilityScope(str, Enum):
    PRIVATE_CONVERSATION = "PRIVATE_CONVERSATION"
    SHARED = "SHARED"


class DocumentReference(BaseModel):
    """Identifies a document version and its access scope."""

    model_config = ConfigDict(extra="forbid")

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


class EvidenceRecord(BaseModel):
    """Represents evidence extracted from a document."""

    model_config = ConfigDict(extra="forbid")

    evidence_id: UUID
    source: DocumentReference
    content_revision_id: UUID

    content: str = Field(min_length=1)
    page_number: int | None = Field(default=None, ge=1)
    section_reference: str | None = None

    validation_status: str = "PENDING"


class AuthorizedRetrievalRequest(BaseModel):
    """Internal retrieval request after authorization checks."""

    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1)
    requester_user_id: int = Field(gt=0)
    conversation_id: UUID

    authorized_document_version_ids: list[UUID]
    top_k: int = Field(default=5, ge=1, le=20)
