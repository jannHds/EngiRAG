
from uuid import uuid4

import pytest
from pydantic import ValidationError

from contracts.schemas import (
    DocumentReference,
    EvidenceRecord,
    AuthorizedRetrievalRequest,
    VisibilityScope,
)


def test_valid_private_document():
    document = DocumentReference(
        document_id=uuid4(),
        document_version_id=uuid4(),
        visibility_scope=VisibilityScope.PRIVATE_CONVERSATION,
        owner_id=1,
        conversation_id=uuid4(),
    )

    assert document.owner_id == 1
    assert document.visibility_scope == VisibilityScope.PRIVATE_CONVERSATION


def test_private_document_requires_owner():
    with pytest.raises(ValidationError):
        DocumentReference(
            document_id=uuid4(),
            document_version_id=uuid4(),
            visibility_scope=VisibilityScope.PRIVATE_CONVERSATION,
            conversation_id=uuid4(),
        )


def test_private_document_requires_conversation():
    with pytest.raises(ValidationError):
        DocumentReference(
            document_id=uuid4(),
            document_version_id=uuid4(),
            visibility_scope=VisibilityScope.PRIVATE_CONVERSATION,
            owner_id=1,
        )


def test_shared_document_rejects_private_owner():
    with pytest.raises(ValidationError):
        DocumentReference(
            document_id=uuid4(),
            document_version_id=uuid4(),
            visibility_scope=VisibilityScope.SHARED,
            owner_id=1,
        )


def test_evidence_rejects_empty_content():
    source = DocumentReference(
        document_id=uuid4(),
        document_version_id=uuid4(),
        visibility_scope=VisibilityScope.SHARED,
    )

    with pytest.raises(ValidationError):
        EvidenceRecord(
            evidence_id=uuid4(),
            source=source,
            content_revision_id=uuid4(),
            content="",
        )


@pytest.mark.parametrize("top_k", [0, 21])
def test_retrieval_rejects_invalid_top_k(top_k):
    with pytest.raises(ValidationError):
        AuthorizedRetrievalRequest(
            question="What is the operating pressure?",
            requester_user_id=1,
            conversation_id=uuid4(),
            authorized_document_version_ids=[uuid4()],
            top_k=top_k,
        )
