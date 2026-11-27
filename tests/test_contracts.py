
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

# S1-03: Evidence and Retrieval Contract Tests

from uuid import uuid4

import pytest
from pydantic import ValidationError

from contracts.schemas import (
    AuthorizedRetrievalRequest,
    DocumentReference,
    EngineeringFact,
    EvidenceRecord,
    RetrievedChunk,
    RetrievalScores,
    SourceLocation,
    ValidationStatus,
)


def make_approved_evidence():
    return EvidenceRecord(
        evidence_id=uuid4(),
        source=DocumentReference(
            document_id=uuid4(),
            document_version_id=uuid4(),
            visibility_scope="SHARED",
        ),
        content_revision_id=uuid4(),
        content="Pump A operating pressure is 10 bar.",
        validation_status=ValidationStatus.APPROVED,
        source_locations=[
            SourceLocation(
                pdf_page_index=0,
                table_reference="Table 1",
            )
        ],
    )


def make_retrieved_chunk(evidence_records):
    return RetrievedChunk(
        chunk_id=uuid4(),
        chunk_text="Pump A operating pressure is 10 bar.",
        index_generation_id=uuid4(),
        document_title="Pump Specification",
        rank=1,
        retrieval_method="dense",
        scores=RetrievalScores(dense_score=0.91),
        evidence_records=evidence_records,
    )


# Student 2: Structured engineering facts

def test_engineering_fact_preserves_values_and_units():
    fact = EngineeringFact(
        equipment_identifier="Pump A",
        parameter_name="Operating Pressure",
        value_text="10",
        unit="bar",
        header_hierarchy=["Pump A", "Specifications"],
    )

    assert fact.equipment_identifier == "Pump A"
    assert fact.parameter_name == "Operating Pressure"
    assert fact.value_text == "10"
    assert fact.unit == "bar"


def test_engineering_fact_requires_parameter():
    with pytest.raises(ValidationError):
        EngineeringFact(
            parameter_name="",
            value_text="10",
            unit="bar",
        )


# Student 2: Source traceability

def test_source_location_cannot_be_empty():
    with pytest.raises(ValidationError):
        SourceLocation()


def test_source_location_accepts_first_pdf_page():
    location = SourceLocation(
        pdf_page_index=0,
        printed_page_label="i",
        table_reference="Table 2",
        cell_range="B2:D4",
    )

    assert location.pdf_page_index == 0
    assert location.cell_range == "B2:D4"


def test_approved_evidence_requires_source_location():
    with pytest.raises(ValidationError):
        EvidenceRecord(
            evidence_id=uuid4(),
            source=DocumentReference(
                document_id=uuid4(),
                document_version_id=uuid4(),
                visibility_scope="SHARED",
            ),
            content_revision_id=uuid4(),
            content="Operating pressure: 10 bar",
            validation_status="APPROVED",
        )


# Student 2: Validation and extraction confidence

@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_invalid_extraction_confidence(confidence):
    evidence = make_approved_evidence()

    with pytest.raises(ValidationError):
        EvidenceRecord(
            **{
                **evidence.model_dump(),
                "extraction_confidence": confidence,
            }
        )


def test_invalid_validation_status():
    evidence = make_approved_evidence()

    with pytest.raises(ValidationError):
        EvidenceRecord(
            **{
                **evidence.model_dump(),
                "validation_status": "UNKNOWN",
            }
        )


# Student 3: Retrieval validation

def test_retrieval_rejects_unapproved_evidence():
    evidence = make_approved_evidence()
    pending = evidence.model_copy(
        update={"validation_status": ValidationStatus.PENDING}
    )

    with pytest.raises(ValidationError):
        make_retrieved_chunk([pending])


def test_chunk_rejects_mixed_content_revisions():
    first = make_approved_evidence()

    second = first.model_copy(
        update={
            "evidence_id": uuid4(),
            "content_revision_id": uuid4(),
        }
    )

    with pytest.raises(ValidationError):
        make_retrieved_chunk([first, second])


def test_chunk_rejects_mixed_document_versions():
    first = make_approved_evidence()

    second_source = first.source.model_copy(
        update={"document_version_id": uuid4()}
    )

    second = first.model_copy(
        update={
            "evidence_id": uuid4(),
            "source": second_source,
        }
    )

    with pytest.raises(ValidationError):
        make_retrieved_chunk([first, second])


def test_retrieval_request_accepts_new_settings():
    request = AuthorizedRetrievalRequest(
        question="What is the operating pressure?",
        requester_user_id=1,
        conversation_id=uuid4(),
        authorized_document_version_ids=[uuid4()],
        query_language="ar",
        retrieval_mode="hybrid",
        index_generation_id=uuid4(),
        retrieval_profile_id=uuid4(),
    )

    assert request.query_language.value == "ar"
    assert request.retrieval_mode.value == "hybrid"
    assert request.index_generation_id is not None
