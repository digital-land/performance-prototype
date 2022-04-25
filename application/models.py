import uuid

from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import func
from application.extensions import db


class Test(db.Model):
    test = db.Column(db.Text, primary_key=True, nullable=False)
    dataset = db.Column(db.Text, nullable=False)
    organisation = db.Column(db.Text, nullable=False)
    query = db.Column(db.Text, nullable=False)
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_date = db.Column(db.TIMESTAMP, server_default=func.now())
    runs = db.relationship("TestRun", backref="test")
    assertions = db.relationship("Assertion", backref="test")


class Assertion(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    json_path = db.Column(db.Text, nullable=False)
    regex = db.Column(db.Text, nullable=False)
    test_id = db.Column(db.Text, db.ForeignKey("test.test"))


class TestRun(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    test_id = db.Column(db.Text, db.ForeignKey("test.test"))
    results = db.relationship("Result", backref="test_run")


class Result(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = db.Column(db.Text, nullable=False)
    expected = db.Column(db.Text, nullable=False)
    actual = db.Column(db.Text)
    match = db.Column(db.BOOLEAN, default=False)
    test_run_id = db.Column(UUID(as_uuid=True), db.ForeignKey("test_run.id"))
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
