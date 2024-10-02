#!/usr/bin/env python3

import strawberry

@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    role: str