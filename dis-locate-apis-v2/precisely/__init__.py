"""
Precisely API package.

PreciselyAPI is composed from domain-specific mixins, each living in its own module:

    precisely/client.py          — BaseClient: session, auth, _validate_graphql_response
    precisely/geocoding.py       — GeocodingMixin
    precisely/tax_emergency.py   — TaxEmergencyMixin
    precisely/verification.py    — VerificationMixin
    precisely/timezone.py        — TimezoneMixin
    precisely/geolocation.py     — GeolocationMixin
    precisely/property_risk.py   — PropertyRiskMixin
    precisely/demographics.py    — DemographicsMixin
    precisely/graphql_advanced.py — GraphQLAdvancedMixin
    precisely/spatial.py         — SpatialMixin
    precisely/map_services.py    — MapServicesMixin
    precisely/routing.py         — RoutingMixin
"""

from .client import BaseClient
from .geocoding import GeocodingMixin
from .tax_emergency import TaxEmergencyMixin
from .verification import VerificationMixin
from .timezone import TimezoneMixin
from .geolocation import GeolocationMixin
from .property_risk import PropertyRiskMixin
from .demographics import DemographicsMixin
from .graphql_advanced import GraphQLAdvancedMixin
from .spatial import SpatialMixin
from .map_services import MapServicesMixin
from .routing import RoutingMixin


class PreciselyAPI(
    GeocodingMixin,
    TaxEmergencyMixin,
    VerificationMixin,
    TimezoneMixin,
    GeolocationMixin,
    PropertyRiskMixin,
    DemographicsMixin,
    GraphQLAdvancedMixin,
    SpatialMixin,
    MapServicesMixin,
    RoutingMixin,
    BaseClient,
):
    """Precisely API client for all MCP tools across domain modules."""


__all__ = ["PreciselyAPI"]
