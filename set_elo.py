#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:25:46 2023

@author: Jason
"""

from elo_system5 import EloSystem

# Create a new EloSystem object
elo_system = EloSystem()

# Print current player ratings
elo_system.print_ratings()

# Get player names and new rating from user input
player = input("Enter player name: ")
new_rating = int(input("Enter new rating: "))

# Set player's rating to the new value
elo_system.set_elo(player, new_rating)

#save updated rankings
elo_system.save_ratings("ratings.pkl")

# Print updated player ratings
elo_system.print_ratings()
