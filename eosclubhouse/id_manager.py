#!/usr/bin/env python3
"""
Clubhouse ID Management System
Provides comprehensive ID management and token-based linking for Clubhouse application.
"""

import hashlib
import time
import uuid
from enum import Enum
from typing import Dict, List, Optional, Any, Set
from gi.repository import GObject


class IDType(Enum):
    """Enumeration of supported ID types."""
    CLUBHOUSE = "clubhouse"
    USER = "user"
    SESSION = "session"
    QUEST = "quest"
    ACHIEVEMENT = "achievement"
    CUSTOM = "custom"


class TokenStatus(Enum):
    """Enumeration of token states."""
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    PENDING = "pending"


class ClubhouseID(GObject.GObject):
    """Represents a unique identifier with metadata and access tracking."""
    
    def __init__(self, id_type: IDType, metadata: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.id_value = str(uuid.uuid4())
        self.id_type = id_type
        self.metadata = metadata or {}
        self.created_at = time.time()
        self.access_count = 0
        self.last_accessed = None
        
    def get_metadata(self, key: str) -> Any:
        """Get metadata value by key."""
        self.access_count += 1
        self.last_accessed = time.time()
        return self.metadata.get(key)
    
    def set_metadata(self, key: str, value: Any):
        """Set metadata value."""
        self.metadata[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize ID to dictionary."""
        return {
            'id_value': self.id_value,
            'id_type': self.id_type.value,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed
        }


class TokenID(GObject.GObject):
    """Represents a secure token that links two IDs together."""
    
    def __init__(self, source_id: str, target_id: str, expires_in: int = 3600,
                 relationship_type: str = "link", metadata: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.token_value = str(uuid.uuid4())
        self.source_id = source_id
        self.target_id = target_id
        self.relationship_type = relationship_type
        self.metadata = metadata or {}
        self.created_at = time.time()
        self.expires_at = time.time() + expires_in if expires_in > 0 else None
        self.status = TokenStatus.ACTIVE
        self.token_hash = hashlib.sha256(self.token_value.encode()).hexdigest()
    
    def is_expired(self) -> bool:
        """Check if token has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at
    
    def extend_expiry(self, additional_seconds: int):
        """Extend token expiry time."""
        if self.expires_at is not None:
            self.expires_at += additional_seconds
    
    def revoke(self):
        """Revoke the token."""
        self.status = TokenStatus.REVOKED
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize token to dictionary."""
        return {
            'token_value': self.token_value,
            'source_id': self.source_id,
            'target_id': self.target_id,
            'relationship_type': self.relationship_type,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'expires_at': self.expires_at,
            'status': self.status.value,
            'token_hash': self.token_hash
        }


class IDManager(GObject.GObject):
    """Central manager for all ID operations and relationships."""
    
    def __init__(self):
        super().__init__()
        self.ids: Dict[str, ClubhouseID] = {}
        self.tokens: Dict[str, TokenID] = {}
        self.relationships: Dict[str, List[TokenID]] = {}
        self.reverse_relationships: Dict[str, List[TokenID]] = {}
    
    def add_id(self, clubhouse_id: ClubhouseID):
        """Add an ID to the manager."""
        self.ids[clubhouse_id.id_value] = clubhouse_id
    
    def get_id(self, id_value: str) -> Optional[ClubhouseID]:
        """Get an ID by value."""
        return self.ids.get(id_value)
    
    def get_ids_by_type(self, id_type: IDType) -> List[ClubhouseID]:
        """Get all IDs of a specific type."""
        return [id_obj for id_obj in self.ids.values() if id_obj.id_type == id_type]
    
    def add_token(self, token: TokenID):
        """Add a token to the manager."""
        self.tokens[token.token_value] = token
        
        # Update relationships
        if token.relationship_type not in self.relationships:
            self.relationships[token.relationship_type] = []
        self.relationships[token.relationship_type].append(token)
        
        # Update reverse relationships
        if token.target_id not in self.reverse_relationships:
            self.reverse_relationships[token.target_id] = []
        self.reverse_relationships[token.target_id].append(token)
    
    def get_token(self, token_value: str) -> Optional[TokenID]:
        """Get a token by value."""
        return self.tokens.get(token_value)
    
    def get_linked_ids(self, source_id: str) -> List[str]:
        """Get all IDs linked from a source ID."""
        linked_ids = []
        for token in self.tokens.values():
            if token.source_id == source_id and token.status == TokenStatus.ACTIVE and not token.is_expired():
                linked_ids.append(token.target_id)
        return linked_ids
    
    def get_reverse_linked_ids(self, target_id: str) -> List[str]:
        """Get all IDs that link to a target ID."""
        reverse_linked_ids = []
        for token in self.tokens.values():
            if token.target_id == target_id and token.status == TokenStatus.ACTIVE and not token.is_expired():
                reverse_linked_ids.append(token.source_id)
        return reverse_linked_ids
    
    def get_relationships(self, relationship_type: str = None) -> List[TokenID]:
        """Get relationships, optionally filtered by type."""
        if relationship_type is None:
            return list(self.tokens.values())
        return self.relationships.get(relationship_type, [])
    
    def revoke_token(self, token_value: str) -> bool:
        """Revoke a token."""
        token = self.tokens.get(token_value)
        if token:
            token.revoke()
            return True
        return False
    
    def cleanup_expired_tokens(self) -> int:
        """Clean up expired tokens and return count."""
        expired_count = 0
        for token in self.tokens.values():
            if token.is_expired() and token.status == TokenStatus.ACTIVE:
                token.status = TokenStatus.EXPIRED
                expired_count += 1
        return expired_count
    
    def get_statistics(self) -> Dict[str, int]:
        """Get system statistics."""
        active_tokens = sum(1 for token in self.tokens.values() 
                          if token.status == TokenStatus.ACTIVE and not token.is_expired())
        return {
            'total_ids': len(self.ids),
            'total_tokens': len(self.tokens),
            'active_tokens': active_tokens,
            'expired_tokens': sum(1 for token in self.tokens.values() if token.is_expired()),
            'revoked_tokens': sum(1 for token in self.tokens.values() if token.status == TokenStatus.REVOKED)
        }


# Global ID manager instance
_id_manager = None


def get_id_manager() -> IDManager:
    """Get the global ID manager instance."""
    global _id_manager
    if _id_manager is None:
        _id_manager = IDManager()
    return _id_manager


def create_clubhouse_id(id_type: IDType, metadata: Optional[Dict[str, Any]] = None) -> ClubhouseID:
    """Create a new Clubhouse ID."""
    clubhouse_id = ClubhouseID(id_type, metadata)
    get_id_manager().add_id(clubhouse_id)
    return clubhouse_id


def create_token_link(source_id: str, target_id: str, expires_in: int = 3600,
                     relationship_type: str = "link", metadata: Optional[Dict[str, Any]] = None) -> TokenID:
    """Create a token link between two IDs."""
    token = TokenID(source_id, target_id, expires_in, relationship_type, metadata)
    get_id_manager().add_token(token)
    return token


def verify_token_link(token_value: str) -> bool:
    """Verify if a token link is valid."""
    token = get_id_manager().get_token(token_value)
    if token is None:
        return False
    return token.status == TokenStatus.ACTIVE and not token.is_expired()


def follow_via_token(follower_id: str, followee_id: str, authorizer_token: str) -> Optional[TokenID]:
    """
    Create a follow relationship between two IDs using an authorizer token.
    
    Args:
        follower_id: The ID that will follow
        followee_id: The ID to be followed
        authorizer_token: Token from an ID that has permission to create this relationship
    
    Returns:
        TokenID if successful, None if authorization fails
    """
    # Verify the authorizer token is valid
    if not verify_token_link(authorizer_token):
        return None
    
    # Get the authorizer token details
    manager = get_id_manager()
    auth_token = manager.get_token(authorizer_token)
    if auth_token is None:
        return None
    
    # Create the follow relationship
    follow_token = create_token_link(
        source_id=follower_id,
        target_id=followee_id,
        expires_in=86400,  # 24 hours
        relationship_type="follow",
        metadata={
            "authorized_by": auth_token.source_id,
            "authorized_at": time.time()
        }
    )
    
    return follow_token