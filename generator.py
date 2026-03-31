import pandas as pd
import itertools


# --- CONFIGURATION DU PLATEAU ---
# 1 = X, -1 = O, 0 = Vide

def check_winner(board):
    """Vérifie si un joueur a gagné ou s'il y a match nul."""
    win_conf = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for a, b, c in win_conf:
        if board[a] == board[b] == board[c] and board[a] != 0:
            return board[a]  # Retourne 1 (X) ou -1 (O)
    if 0 not in board:
        return 0  # Match nul
    return None  # Partie en cours


def minimax(board, is_maximizing):
    """Algorithme Minimax pour déterminer l'issue théorique."""
    res = check_winner(board)
    if res is not None:
        return res

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = 1
                score = minimax(board, False)
                board[i] = 0
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = -1
                score = minimax(board, True)
                board[i] = 0
                best_score = min(score, best_score)
        return best_score


def generate_dataset():
    """Génère tous les états valides où c'est au tour de X."""
    print("Génération du dataset en cours... Cela peut prendre 1 à 2 minutes.")
    data = []

    # Parcourir toutes les combinaisons possibles (3^9)
    for board in itertools.product([0, 1, -1], repeat=9):
        board = list(board)

        # Filtre 1 : Nombre de pions (X doit être égal à O car c'est au tour de X)
        nx = board.count(1)
        no = board.count(-1)
        if nx != no:
            continue

        # Filtre 2 : La partie ne doit pas déjà être terminée
        if check_winner(board) is not None:
            continue

        # Calcul de l'issue théorique (Jeu parfait)
        # On suppose que X joue de manière optimale à partir de cet état [cite: 23]
        res = minimax(board, True)

        # Encodage binaire (18 features : c0_x, c0_o, ..., c8_x, c8_o) [cite: 19]
        row = []
        for i in range(9):
            row.append(1 if board[i] == 1 else 0)  # ci_x
            row.append(1 if board[i] == -1 else 0)  # ci_o

        # Ajout des cibles (Targets) [cite: 21]
        row.append(1 if res == 1 else 0)  # x_wins
        row.append(1 if res == 0 else 0)  # is_draw

        data.append(row)

    # Définition des noms de colonnes
    columns = []
    for i in range(9):
        columns.extend([f'c{i}_x', f'c{i}_o'])
    columns.extend(['x_wins', 'is_draw'])

    # Création du DataFrame et export CSV
    df = pd.DataFrame(data, columns=columns)

    # Créer le dossier ressources s'il n'existe pas
    import os
    if not os.path.exists('ressources'):
        os.makedirs('ressources')

    df.to_csv('ressources/dataset.csv', index=False)
    print(f"Succès ! Dataset généré : {len(df)} lignes enregistrées dans 'ressources/dataset.csv'.")


if __name__ == "__main__":
    generate_dataset()