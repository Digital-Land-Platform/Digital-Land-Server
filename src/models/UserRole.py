#!/usr/bin/env python3

import enum

class UserRole(enum.Enum):
    LAND_OWNER = "Land Owner"
    BUYER = "Buyer"
    NOTARY = "Notary"
    ADMIN = "Admin"