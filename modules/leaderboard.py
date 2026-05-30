"""

=============================================================
leaderboard.py — Brickz
=============================================================
Handles all leaderboard functionality as a standalone module.

Scores are stored as a JSON list of dicts at SCORES_FILE in
the user's home directory. Each entry has two keys:
    {"name": "AAA", "score": 42}

-------------------------------------------------------------
FUNCTIONS
-------------------------------------------------------------
load_scores()
    Reads and returns the scores list from the JSON file.
    Returns an empty list if the file doesn't exist or is
    malformed.

save_scores(scores)
    Writes the scores list to the JSON file.

insert_high_score(game)
    Compares game.final_score against the stored scores.
    If it qualifies, appends a placeholder entry, sorts and
    trims to MAX_ENTRIES, stores the index of the new entry
    in game.new_score_index, and sets game.entering_name True.

enter_name(event, game)
    Called on each KEYDOWN event during name entry.
    Builds game.pending_name one character at a time,
    updates the placeholder entry in game.scores in place,
    and saves to disk when 3 characters are complete.

display_leaderboard(game, font, window, WINDOW_WIDTH, WINDOW_HEIGHT)
    Renders the full scores table to the window each frame.
    If game.entering_name is True, redraws the active entry
    with a blinking cursor over the placeholder characters.

-------------------------------------------------------------
DEPENDENCIES
-------------------------------------------------------------
Requires pygame, json, os.path.

game, font, window, WINDOW_WIDTH, WINDOW_HEIGHT are passed
in as parameters

"""

from os.path import join, expanduser
import json
import pygame

SCORES_FILE = join(expanduser("~"), ".p0n6_fl1p_scores.json")
MAX_ENTRIES = 10

def enter_name(event, game):
    if game.entering_name:
        if event.key == pygame.K_BACKSPACE:
            game.pending_name = game.pending_name[:-1]
        elif len(game.pending_name) < 3 and event.unicode.isalpha():
            game.pending_name += event.unicode.upper()
        game.scores[game.new_score_index]["name"] = game.pending_name.ljust(3, "_")
        if len(game.pending_name) == 3:
            save_scores(game.scores)
            game.entering_name = False

def load_scores():
    try:
        with open(SCORES_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except:
        return []

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

def insert_high_score(game):
    if len(game.scores) < MAX_ENTRIES or game.final_score > game.scores[-1]["score"]:
        game.scores.append({"name": "___", "score": game.final_score})
        game.scores = sorted(game.scores, key=lambda x: x["score"], reverse=True)[:MAX_ENTRIES]
        game.new_score_index = next(i for i, e in enumerate(game.scores) if e["name"] == "___")
        game.entering_name = True

def display_leaderboard(game, font, window, WINDOW_WIDTH, WINDOW_HEIGHT):
    for i, entry in enumerate(game.scores):
        name = entry["name"]
        text = f"{i+1:02}  {name:<3}  {entry['score']:>6}"
        text_surf = font.render(text, True, (240, 240, 240))
        text_rect = text_surf.get_frect(midleft=(WINDOW_WIDTH / 2 - 150, 120 + i * 35))
        window.blit(text_surf, text_rect)

    if game.entering_name:
        show_cursor = (pygame.time.get_ticks() // 500) % 2 == 0
        chars = list(game.scores[game.new_score_index]["name"])
        cursor_pos = len(game.pending_name)
        if not show_cursor:
            chars[cursor_pos] = " "
        name = "".join(chars)
        text = f"{game.new_score_index+1:02}  {name:<3}  {game.scores[game.new_score_index]['score']:>6}"
        text_surf = font.render(text, True, (240, 240, 240))
        text_rect = text_surf.get_frect(midleft=(WINDOW_WIDTH / 2 - 150, 120 + game.new_score_index * 35))
        window.blit(text_surf, text_rect)
        prompt_surf = font.render("ENTER YOUR INITIALS", True, (240, 240, 240))
        prompt_rect = prompt_surf.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 150))
        window.blit(prompt_surf, prompt_rect)