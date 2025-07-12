"""
EOS Clubhouse ID Management System

This package provides comprehensive ID management and token-based linking
for the Clubhouse application.
"""

from .id_manager import (
    IDType,
    TokenStatus,
    ClubhouseID,
    TokenID,
    IDManager,
    get_id_manager,
    create_clubhouse_id,
    create_token_link,
    verify_token_link,
    follow_via_token
)

__version__ = "1.0.0"
__all__ = [
    "IDType",
    "TokenStatus", 
    "ClubhouseID",
    "TokenID",
    "IDManager",
    "get_id_manager",
    "create_clubhouse_id",
    "create_token_link",
    "verify_token_link",
    "follow_via_token"
]