"""
Precisely API package.

PreciselyAPI is composed from domain-specific mixins, each living in its own module:

    precisely/client.py          — BaseClient: session, auth, _validate_graphql_response
    precisely/geocoding.py       — GeocodingMixin (9 methods)
    precisely/tax_emergency.py   — TaxEmergencyMixin (9 methods)
    precisely/verification.py    — VerificationMixin (5 methods)
    precisely/timezone.py        — TimezoneMixin (2 methods)
    precisely/geolocation.py     — GeolocationMixin (2 methods)
    precisely/property_risk.py   — PropertyRiskMixin (9 methods)
    precisely/demographics.py    — DemographicsMixin (8 methods)
    precisely/graphql_advanced.py — GraphQLAdvancedMixin (5 methods)
    precisely/spatial.py         — SpatialMixin (7 methods)
    precisely/map_services.py    — MapServicesMixin (15 methods)
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
    BaseClient,
):
    """Precisely API client — all 71 methods across 10 domain modules."""


__all__ = ["PreciselyAPI"]
