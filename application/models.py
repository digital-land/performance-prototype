import uuid

from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import func
from application.extensions import db


class TestRun(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    results = db.relationship("Result", backref="test_run", cascade="all,delete")


class Result(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_name = db.Column(db.Text, nullable=False)
    dataset = db.Column(db.Text, nullable=False)
    organisation = db.Column(db.Text, nullable=False)
    query = db.Column(db.Text, nullable=False)
    ticket = db.Column(db.Text, nullable=True)
    test_run_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("test_run.id"), nullable=False
    )
    response_data_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("response_data.id"), nullable=False
    )
    assertions = db.relationship(
        "Assertion", backref="test_result", cascade="all,delete"
    )


class Assertion(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = db.Column(db.Text, nullable=False)
    expected = db.Column(db.Text, nullable=False)
    actual = db.Column(db.Text)
    match = db.Column(db.BOOLEAN, default=False)
    test_result_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("result.id"), nullable=False
    )


class ResponseData(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    test_name = db.Column(db.Text, nullable=False)
    query = db.Column(db.Text, nullable=False)
    data = db.Column(JSONB, nullable=True)
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    results = db.relationship("Result", backref="response_data", cascade="all,delete")
