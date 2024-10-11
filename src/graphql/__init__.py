# src/graphql/__init__.py
"""
graphql - Main package for the GraphQL API.

This package contains the GraphQL schema and entry points for the application.
It integrates various modules and handles user-related operations through 
mutations and queries.

Modules:
- index: Main entry for GraphQL, combining various schemas.
- users: User-related GraphQL logic, including queries, mutations, and type definitions.
"""
from .index import schema
