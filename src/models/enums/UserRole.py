#!/usr/bin/env python3

import enum

class UserRole(enum.Enum):
    BROKER = "Broker"
    USER = "User"
    NOTARY = "Notary"
    ADMIN = "Admin"