#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 23:19:53 2023

@author: Jason
"""

from elo_system5 import EloSystem

# Create EloSystem object
elo_system = EloSystem()

# Print ratings from file
print(elo_system.print_ratings())
