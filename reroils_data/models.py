"""Define relation between records and buckets."""

from __future__ import absolute_import

from invenio_db import db
from invenio_records.models import RecordMetadata
from sqlalchemy_utils.types import UUIDType


class RecordsItems(db.Model):
    """Relationship between Records and Circulation Items."""

    __tablename__ = 'records_crcitm'

    record_id = db.Column(
        UUIDType,
        db.ForeignKey(RecordMetadata.id),
        primary_key=True,
        nullable=False,
        # NOTE no unique constrain for better future ...
    )
    """Record related with the item."""

    item_id = db.Column(
        UUIDType,
        db.ForeignKey(RecordMetadata.id),
        primary_key=True,
        nullable=False,
        # NOTE no unique constrain for better future ...
    )
    """Item related with the record."""

    item = db.relationship(RecordMetadata, foreign_keys=[item_id])
    """Relationship to the item."""

    record = db.relationship(RecordMetadata, foreign_keys=[record_id])
    """It is used by SQLAlchemy for optimistic concurrency control."""

    @classmethod
    def create(cls, record, item):
        """Create a new RecordsItem and adds it to the session.

        :param record: Record used to relate with the ``Item``.
        :param item: Item used to relate with the ``Record``.
        :returns: The :class:`~invenio_records_files.models.RecordsItems`
            object created.
        """
        rb = cls(record=record, item=item)
        db.session.add(rb)
        return rb
