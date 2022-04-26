import uuid

from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import func
from application.extensions import db


test_runs = db.Table(
    "test_runs",
    db.metadata,
    db.Column("test_id", db.ForeignKey("test.test")),
    db.Column("test_run_id", db.ForeignKey("test_run.id")),
)


class TestRun(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    results = db.relationship("Result", backref="test_run")
    tests = db.relationship("Test", secondary=test_runs, lazy=True)


class Test(db.Model):
    test = db.Column(db.Text, primary_key=True, nullable=False)
    dataset = db.Column(db.Text, nullable=False)
    organisation = db.Column(db.Text, nullable=False)
    ticket = db.Column(db.Text, nullable=True)
    query = db.Column(db.Text, nullable=False)
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_date = db.Column(db.TIMESTAMP, server_default=func.now())
    assertions = db.relationship("Assertion", backref="test")
    test_runs = db.relationship(
        "TestRun", secondary=test_runs, lazy=True, viewonly=True
    )


class Assertion(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    json_path = db.Column(db.Text, nullable=False)
    regex = db.Column(db.Text, nullable=False)
    test_id = db.Column(db.Text, db.ForeignKey("test.test"))


class Result(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = db.Column(db.Text, nullable=False)
    expected = db.Column(db.Text, nullable=False)
    actual = db.Column(db.Text)
    match = db.Column(db.BOOLEAN, default=False)
    data = db.Column(JSONB, nullable=True)
    test_run_id = db.Column(UUID(as_uuid=True), db.ForeignKey("test_run.id"))
    test_id = db.Column(db.Text, db.ForeignKey("test.test"))
    created_timestamp = db.Column(db.TIMESTAMP, server_default=func.now())

