"""Generated implementation of scheduler."""

# WARNING DO NOT EDIT
# This code was generated from scheduler.mcn

from __future__ import annotations

import abc  # noqa: F401
import dataclasses  # noqa: F401
import datetime  # noqa: F401
import enum  # noqa: F401
import isodate  # noqa: F401
import json  # noqa: F401
import jsonschema  # noqa: F401
import logging  # noqa: F401
import typing  # noqa: F401
import uuid  # noqa: F401
try:
    from anaml_client.utils.serialisation import JsonObject  # noqa: F401
except ImportError:
    pass

from ..cluster import ClusterPropertySetId
from ..date_range import DateRange
from ..event_store import EventStoreId
from ..feature_store import FeatureStoreId
from ..source_reference import SourceReference
from ..table_caching import TableCachingJobId
from ..table_monitoring import TableMonitoringJobId
from ..view_materialisation import ViewMaterialisationJobId


@dataclasses.dataclass(frozen=True)
class SchedulerRunRequest:
    """A request for the scheduler to immediately kick off a job.
    
    Only one job id should be set in each call to the
    endpoint.
    
    If the job is an event store batch run, then also include
    a subject and source.
    
    Args:
        featureStoreId (typing.Optional[FeatureStoreId]): A data field.
        tableMonitoringJobId (typing.Optional[TableMonitoringJobId]): A data field.
        tableCachingJobId (typing.Optional[TableCachingJobId]): A data field.
        viewMaterialisationJobId (typing.Optional[ViewMaterialisationJobId]): A data field.
        eventStoreId (typing.Optional[EventStoreId]): A data field.
        dateRange (typing.Optional[DateRange]): A data field.
        subject (typing.Optional[str]): A data field.
        source (typing.Optional[SourceReference]): A data field.
        clusterPropertySets (typing.Optional[typing.List[ClusterPropertySetId]]): A data field.
    """
    
    featureStoreId: typing.Optional[FeatureStoreId]
    tableMonitoringJobId: typing.Optional[TableMonitoringJobId]
    tableCachingJobId: typing.Optional[TableCachingJobId]
    viewMaterialisationJobId: typing.Optional[ViewMaterialisationJobId]
    eventStoreId: typing.Optional[EventStoreId]
    dateRange: typing.Optional[DateRange]
    subject: typing.Optional[str]
    source: typing.Optional[SourceReference]
    clusterPropertySets: typing.Optional[typing.List[ClusterPropertySetId]]
    
    @classmethod
    def json_schema(cls) -> dict:
        """Return the JSON schema for SchedulerRunRequest data.
        
        Returns:
            A Python dictionary describing the JSON schema.
        """
        return {
            "type": "object",
            "properties": {
                "featureStoreId": {
                    "oneOf": [
                        {"type": "null"},
                        FeatureStoreId.json_schema(),
                    ]
                },
                "tableMonitoringJobId": {
                    "oneOf": [
                        {"type": "null"},
                        TableMonitoringJobId.json_schema(),
                    ]
                },
                "tableCachingJobId": {
                    "oneOf": [
                        {"type": "null"},
                        TableCachingJobId.json_schema(),
                    ]
                },
                "viewMaterialisationJobId": {
                    "oneOf": [
                        {"type": "null"},
                        ViewMaterialisationJobId.json_schema(),
                    ]
                },
                "eventStoreId": {
                    "oneOf": [
                        {"type": "null"},
                        EventStoreId.json_schema(),
                    ]
                },
                "dateRange": {
                    "oneOf": [
                        {"type": "null"},
                        DateRange.json_schema(),
                    ]
                },
                "subject": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "string"},
                    ]
                },
                "source": {
                    "oneOf": [
                        {"type": "null"},
                        SourceReference.json_schema(),
                    ]
                },
                "clusterPropertySets": {
                    "oneOf": [
                        {"type": "null"},
                        {"type": "array", "item": ClusterPropertySetId.json_schema()},
                    ]
                }
            },
            "required": []
        }
    
    @classmethod
    def from_json(cls, data: dict) -> SchedulerRunRequest:
        """Validate and parse JSON data into an instance of SchedulerRunRequest.
        
        Args:
            data (dict): JSON data to validate and parse.
        
        Returns:
            An instance of SchedulerRunRequest.
        
        Raises:
            ValidationError: When schema validation fails.
            KeyError: When a required field is missing from the JSON.
        """
        try:
            jsonschema.validate(data, cls.json_schema())
            return SchedulerRunRequest(
                featureStoreId=(
                    lambda v: v and FeatureStoreId.from_json(v)
                )(
                    data.get("featureStoreId", None)
                ),
                tableMonitoringJobId=(
                    lambda v: v and TableMonitoringJobId.from_json(v)
                )(
                    data.get("tableMonitoringJobId", None)
                ),
                tableCachingJobId=(
                    lambda v: v and TableCachingJobId.from_json(v)
                )(
                    data.get("tableCachingJobId", None)
                ),
                viewMaterialisationJobId=(
                    lambda v: v and ViewMaterialisationJobId.from_json(v)
                )(
                    data.get("viewMaterialisationJobId", None)
                ),
                eventStoreId=(
                    lambda v: v and EventStoreId.from_json(v)
                )(
                    data.get("eventStoreId", None)
                ),
                dateRange=(lambda v: v and DateRange.from_json(v))(data.get("dateRange", None)),
                subject=(lambda v: v and str(v))(data.get("subject", None)),
                source=(lambda v: v and SourceReference.from_json(v))(data.get("source", None)),
                clusterPropertySets=(
                    lambda v: v and [ClusterPropertySetId.from_json(v) for v in v]
                )(
                    data.get("clusterPropertySets", None)
                ),
            )
        except jsonschema.exceptions.ValidationError as ex:
            logging.debug(
                "Invalid JSON data received while parsing SchedulerRunRequest",
                exc_info=ex
            )
            raise
    
    def to_json(self) -> dict:
        """Serialise this instance as JSON.
        
        Returns:
            Data ready to serialise as JSON.
        """
        return {
            "featureStoreId": (lambda v: v and v.to_json())(self.featureStoreId),
            "tableMonitoringJobId": (lambda v: v and v.to_json())(self.tableMonitoringJobId),
            "tableCachingJobId": (lambda v: v and v.to_json())(self.tableCachingJobId),
            "viewMaterialisationJobId": (lambda v: v and v.to_json())(self.viewMaterialisationJobId),
            "eventStoreId": (lambda v: v and v.to_json())(self.eventStoreId),
            "dateRange": (lambda v: v and v.to_json())(self.dateRange),
            "subject": (lambda v: v and str(v))(self.subject),
            "source": (lambda v: v and v.to_json())(self.source),
            "clusterPropertySets": (lambda v: v and [v.to_json() for v in v])(self.clusterPropertySets)
        }
