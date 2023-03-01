#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 22:42:49 2023

@author: Jason
"""

from elo_system5 import EloSystem

# Create EloSystem object
elo_system = EloSystem()

# Load saved ratings from file if it exists
try:
    elo_system.load_ratings("ratings.pkl")
except FileNotFoundError:
    pass

# Get input from user for winner and loser names
winner = input("Enter the name of the winner: ")
loser = input("Enter the name of the loser: ")

# Update ratings for winner and loser
elo_system.update_rating(winner, loser)

# Print updated ratings
elo_system.print_ratings()

# Save updated ratings to file
elo_system.save_ratings("ratings.pkl")
