#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:23:05 2023

@author: Jason
"""

import pickle
from operator import itemgetter
class EloSystem:
    def __init__(self, K=32):
        self.K = K
        self.ratings = {}
        self.num_games = {}
        self.num_wins = {}
        self.num_losses = {}

    def update_rating(self, winner, loser):
        # Convert player names to lowercase
        winner = winner.lower()
        loser = loser.lower()

        # Check if winner and loser are already in the ratings dictionary
        if winner not in self.ratings:
            self.ratings[winner] = 1000
            self.num_games[winner] = 0
            self.num_wins[winner] = 0
            self.num_losses[winner] = 0
        if loser not in self.ratings:
            self.ratings[loser] = 1000
            self.num_games[loser] = 0
            self.num_wins[loser] = 0
            self.num_losses[loser] = 0

        # Calculate expected win probability for winner
        rating_diff = self.ratings[winner] - self.ratings[loser]
        expected_win_prob = 1 / (1 + 10 ** (-rating_diff / 400))

        # Update ratings for winner and loser
        self.ratings[winner] += self.K * (1 - expected_win_prob)
        self.ratings[loser] -= self.K * expected_win_prob

        # Update game counts for winner and loser
        self.num_games[winner] += 1
        self.num_games[loser] += 1
        self.num_wins[winner] += 1
        self.num_losses[loser] += 1
        
        self.save_ratings("ratings.pkl")
    
    def set_elo(self, player, rating):
        
        if player not in self.ratings:
            print(f"{player} is not in the ratings list. Cannot set ELO rating.")
            return
        self.ratings[player] = rating
    
        # Save updated ratings to ratings.pkl file
        with open('ratings.pkl', 'wb') as f:
            pickle.dump(self.ratings, f)
            
            
            
            pickle.dump(self.num_games, f)
            pickle.dump(self.num_wins, f)
            pickle.dump(self.num_losses, f)
            

       
       #if player not in self.ratings:
            """self.ratings[player] = 1000
        self.ratings[player] = rating

        # Save updated ratings to ratings.pkl file
        with open('ratings.pkl', 'wb') as f:
            pickle.dump(self.ratings, f)"""
    
    
    def print_ratings(self):
        try:
            # Load ratings from file
            with open("ratings.pkl", "rb") as f:
                self.ratings = pickle.load(f)
                self.num_games = pickle.load(f)
                self.num_wins = pickle.load(f)
                self.num_losses = pickle.load(f)
                
    
            # Check the data type of the first value in the dictionary
            first_value = next(iter(self.ratings.values()))
            value_type = type(first_value)
    
            # Convert all values to the same data type
            self.ratings = {k: value_type(v) for k, v in self.ratings.items()}
    
            # Sort ratings by rating in descending order
            sorted_ratings = sorted(self.ratings.items(), key=itemgetter(1), reverse=True)
    
            # Build table header string
            header = "{:<20} {:<10} {:<10} {:<10} {:<10}\n".format("Player", "Rating", "Games", "Wins", "Losses")
            header += "-" * 60 + "\n"
    
            # Build table rows string
            rows = ""
            for player, rating in sorted_ratings:
                games = self.num_games[player]
                wins = self.num_wins[player]
                losses = self.num_losses[player]
                win_pct = round(100 * wins / games) if games > 0 else 0
                rows += "{:<20} {:<10} {:<10} {:<10} {:<10}\n".format(player.capitalize(), rating, games, wins, losses, win_pct)
    
            # Build final output string
            output = header + rows
    
        except FileNotFoundError:
            output = "No ratings file found.\n"
    
        return output



    """def print_ratings(self):
        try:
            # Load ratings from file
            with open("ratings.pkl", "rb") as f:
                self.ratings, self.num_games, self.num_wins, self.num_losses = pickle.load(f)
    
            # Convert all values to float
            self.ratings = {k: float(v) for k, v in self.ratings.items()}
    
            # Sort ratings by rating in descending order
            sorted_ratings = sorted(self.ratings.items(), key=lambda x: x[1], reverse=True)
    
            # Build table header string
            header = "{:<20} {:<10} {:<10} {:<10} {:<10}\n".format("Player", "Rating", "Games", "Wins", "Losses")
            header += "-" * 60 + "\n"
    
            # Build table rows string
            rows = ""
            for player, rating in sorted_ratings:
                games = self.num_games[player]
                wins = self.num_wins[player]
                losses = self.num_losses[player]
                win_pct = round(100 * wins / games) if games > 0 else 0
                rows += "{:<20} {:<10.1f} {:<10} {:<10} {:<10}\n".format(player.capitalize(), rating, games, wins, losses, win_pct)
    
            # Build final output string
            output = header + rows
    
        except FileNotFoundError:
            output = "No ratings file found.\n"
    
        return output"""






    """def print_ratings(self):
        try:
            # Load ratings from file
            with open("ratings.pkl", "rb") as f:
                self.ratings = pickle.load(f)
                self.num_games = pickle.load(f)
                self.num_wins = pickle.load(f)
                self.num_losses = pickle.load(f)
                
            
    
            # Sort ratings by rating in descending order
            sorted_ratings = sorted(self.ratings.items(), key=lambda x: x[1], reverse=True)
    
            # Build table header string
            header = "{:<20} {:<10} {:<10} {:<10} {:<10}\n".format("Player", "Rating", "Games", "Wins", "Losses")
            header += "-" * 60 + "\n"
    
            # Build table rows string
            rows = ""
            for player, rating in sorted_ratings:
                games = self.num_games[player]
                wins = self.num_wins[player]
                losses = self.num_losses[player]
                win_pct = round(100 * wins / games) if games > 0 else 0
                rows += "{:<20} {:<10} {:<10} {:<10} {:<10}\n".format(player.capitalize(), round(rating), games, wins, losses, win_pct)
    
            # Build final output string
            output = header + rows
    
        except FileNotFoundError:
            output = "No ratings file found.\n"
    
        return output"""

    



    def save_ratings(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self.ratings, f)
            pickle.dump(self.num_games, f)
            pickle.dump(self.num_wins, f)
            pickle.dump(self.num_losses, f)
        

    def load_ratings(self, filename):
        try:
            with open(filename, "rb") as f:
                self.ratings = pickle.load(f)
                self.num_games = pickle.load(f)
                self.num_wins = pickle.load(f)
                self.num_losses = pickle.load(f)
        except EOFError:
            self.ratings = {}
            self.num_games = {}