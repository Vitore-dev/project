from datetime import datetime
from . import db
from flask_sqlalchemy import SQLAlchemy

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey,
    Text, Enum, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from . import db

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(Enum("doctor", "nurse", "admin", name="user_roles"), nullable=False)

    license_number = Column(String(100))
    specialty = Column(String(100))
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime)

    encounters = relationship("Encounter", back_populates="provider")


class Patient(db.Model, TimestampMixin):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    national_id = Column(String(50), index=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    sex = Column(Enum("male", "female", "other", name="sex_enum"), nullable=False)

    phone = Column(String(20))
    address_line = Column(String(255))
    city = Column(String(100))
    district = Column(String(100))

    blood_type = Column(String(5))
    hiv_status = Column(String(50))
    is_deceased = Column(Boolean, default=False)
    deceased_date = Column(DateTime)

    encounters = relationship("Encounter", back_populates="patient")
    allergies = relationship("Allergy", back_populates="patient")


class Encounter(db.Model, TimestampMixin):
    __tablename__ = "encounters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    encounter_type = Column(String(50))  # OPD, HIV, TB, etc.
    status = Column(Enum("draft", "signed", "cancelled", name="encounter_status"), default="draft")

    chief_complaint = Column(Text)
    priority = Column(Enum("routine", "urgent", "emergency", name="priority_enum"))

    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    signed_at = Column(DateTime)

    patient = relationship("Patient", back_populates="encounters")
    provider = relationship("User", back_populates="encounters")

    notes = relationship("Note", back_populates="encounter")
    diagnoses = relationship("Diagnosis", back_populates="encounter")
    medications = relationship("Medication", back_populates="encounter")
    lab_orders = relationship("LabOrder", back_populates="encounter")


class Note(db.Model, TimestampMixin):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    subjective = Column(Text)
    objective = Column(Text)
    assessment = Column(Text)
    plan = Column(Text)

    transcript_text = Column(Text)
    ai_generated = Column(Boolean, default=False)
    confidence_score = Column(Integer)

    version = Column(Integer, default=1)
    is_locked = Column(Boolean, default=False)

    encounter = relationship("Encounter", back_populates="notes")


class Diagnosis(db.Model, TimestampMixin):
    __tablename__ = "diagnoses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)

    icd10_code = Column(String(20), nullable=False)
    description = Column(String(255))

    clinical_status = Column(String(50))  # active/resolved
    verification_status = Column(String(50))  # provisional/confirmed
    is_primary = Column(Boolean, default=False)
    onset_date = Column(DateTime)

    ai_suggested = Column(Boolean, default=False)
    confidence_score = Column(Integer)

    encounter = relationship("Encounter", back_populates="diagnoses")


class Medication(db.Model, TimestampMixin):
    __tablename__ = "medications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    prescriber_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    drug_name = Column(String(255), nullable=False)
    dosage = Column(String(100))
    route = Column(String(100))
    frequency = Column(String(100))
    duration = Column(String(100))

    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(50))  # active/completed/stopped

    ai_suggested = Column(Boolean, default=False)

    encounter = relationship("Encounter", back_populates="medications")


class LabOrder(db.Model, TimestampMixin):
    __tablename__ = "lab_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    encounter_id = Column(UUID(as_uuid=True), ForeignKey("encounters.id"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    ordered_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    test_name = Column(String(255), nullable=False)
    loinc_code = Column(String(50))
    priority = Column(String(50))

    status = Column(String(50))  # ordered/completed/cancelled
    result_value = Column(String(100))
    result_unit = Column(String(50))
    reference_range = Column(String(100))
    result_flag = Column(String(50))  # normal/high/low/critical

    ordered_at = Column(DateTime, default=datetime.utcnow)
    resulted_at = Column(DateTime)

    encounter = relationship("Encounter", back_populates="lab_orders")



class Allergy(db.Model, TimestampMixin):
    __tablename__ = "allergies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    recorded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    substance = Column(String(255), nullable=False)
    reaction = Column(String(255))
    severity = Column(String(50))  # mild/moderate/severe
    onset_date = Column(DateTime)
    status = Column(String(50))  # active/resolved

    patient = relationship("Patient", back_populates="allergies")



class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    action = Column(String(100), nullable=False)
    entity_type = Column(String(100))
    entity_id = Column(String(100))

    ip_address = Column(String(50))
    user_agent = Column(String(255))

    timestamp = Column(DateTime, default=datetime.utcnow)

