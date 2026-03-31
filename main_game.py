import customtkinter as ctk
import joblib
import numpy as np
import tkinter.messagebox as messagebox

# Configuration visuelle "Aesthetic"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



class MorpionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ISPM Hackathon - IA Morpion")
        self.geometry("500x750")

        # 1. Chargement des modèles entraînés à l'étape 3
        try:
            self.model_wins = joblib.load('models/best_model_wins.pkl')
            self.model_draw = joblib.load('models/best_model_draw.pkl')
        except:
            print("Erreur : Modèles non trouvés. Vérifiez le dossier 'models/'.")

        self.board = [0] * 9  # 0: vide, 1: X, -1: O
        self.current_player = 1  # X commence toujours
        self.game_mode = ctk.StringVar(value="Humain vs Humain")

        self.setup_ui()

    def setup_ui(self):
        # Titre
        self.label_title = ctk.CTkLabel(self, text="JEUX DE MORPION - NJS", font=("Roboto", 24, "bold"))
        self.label_title.pack(pady=20)

        # Sélecteur de Mode
        self.mode_menu = ctk.CTkOptionMenu(self, values=["Humain vs Humain", "Humain vs IA", "Mode Hybride"],
                                           variable=self.game_mode, command=self.reset_game)
        self.mode_menu.pack(pady=10)

        # Grille de jeu
        self.grid_frame = ctk.CTkFrame(self)
        self.grid_frame.pack(pady=20)

        self.buttons = []
        for i in range(9):
            btn = ctk.CTkButton(self.grid_frame, text="", width=100, height=100,
                                font=("Roboto", 32, "bold"),
                                fg_color="#2b2b2b", hover_color="#3d3d3d",
                                command=lambda i=i: self.on_click(i))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Zone d'analyse IA
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=20, fill="x", padx=40)

        self.label_win = ctk.CTkLabel(self.stats_frame, text="Probabilité Victoire X : --%", font=("Roboto", 14))
        self.label_win.pack(pady=5)

        self.label_draw = ctk.CTkLabel(self.stats_frame, text="Probabilité Match Nul : --%", font=("Roboto", 14))
        self.label_draw.pack(pady=5)

        self.btn_reset = ctk.CTkButton(self, text="Réinitialiser", command=self.reset_game, fg_color="transparent",
                                       border_width=2)
        self.btn_reset.pack(pady=20)

    def encode_board(self, board_state):
        """Encode le plateau en 18 colonnes binaires comme à l'étape 0/2."""
        encoded = []
        for cell in board_state:
            encoded.append(1 if cell == 1 else 0)  # ci_x
            encoded.append(1 if cell == -1 else 0)  # ci_o
        return np.array(encoded).reshape(1, -1)

    def on_click(self, i):
        if self.board[i] == 0:
            self.make_move(i, self.current_player)

            # Si le jeu continue et que c'est le tour de l'IA
            if not self.check_end_game():
                if self.game_mode.get() != "Humain vs Humain":
                    self.after(500, self.ai_turn)

    def make_move(self, i, player):
        self.board[i] = player
        symbol = "X" if player == 1 else "O"
        color = "#1f538d" if player == 1 else "#a83232"
        self.buttons[i].configure(text=symbol, state="disabled", fg_color=color)

        # Mise à jour des prédictions ML en temps réel
        self.update_ml_stats()
        self.current_player *= -1

    def update_ml_stats(self):
        """Utilise les modèles pour afficher l'analyse en temps réel."""
        encoded = self.encode_board(self.board)
        p_win = self.model_wins.predict_proba(encoded)[0][1]
        p_draw = self.model_draw.predict_proba(encoded)[0][1]

        self.label_win.configure(text=f"Probabilité Victoire X : {p_win * 100:.1f}%")
        self.label_draw.configure(text=f"Probabilité Match Nul : {p_draw * 100:.1f}%")

    def ai_turn(self):
        mode = self.game_mode.get()
        best_move = None

        if mode == "Humain vs IA":
            best_move = self.get_ml_move()
        elif mode == "Mode Hybride":
            best_move = self.get_hybrid_move()

        if best_move is not None:
            self.make_move(best_move, self.current_player)
            self.check_end_game()

    def get_ml_move(self):
        """L'IA joue le coup qui maximise sa probabilité de victoire selon le modèle."""
        best_score = -1
        move = None
        for i in range(9):
            if self.board[i] == 0:
                temp_board = list(self.board)
                temp_board[i] = -1  # IA simule son coup (O)
                # Note : On regarde la proba de victoire de X (le modèle a été entraîné sur X)
                # L'IA (O) cherche donc à MINIMISER la proba de victoire de X.
                score = 1 - self.model_wins.predict_proba(self.encode_board(temp_board))[0][1]
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def get_hybrid_move(self):
        """Mode Hybride : Combine une vérification de victoire immédiate et le ML."""
        # 1. Vérifier si l'IA peut gagner au prochain coup (Logique déterministe)
        for i in range(9):
            if self.board[i] == 0:
                temp_board = list(self.board)
                temp_board[i] = -1
                if self.is_winner(temp_board, -1): return i

        # 2. Sinon, utiliser le ML pour évaluer la meilleure position
        return self.get_ml_move()

    def is_winner(self, b, p):
        win_conf = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        return any(b[z[0]] == b[z[1]] == b[z[2]] == p for z in win_conf)

    def check_end_game(self):
        if self.is_winner(self.board, 1):
            messagebox.showinfo("Fin", "X a gagné !")
            self.reset_game()
            return True
        if self.is_winner(self.board, -1):
            messagebox.showinfo("Fin", "O a gagné !")
            self.reset_game()
            return True
        if 0 not in self.board:
            messagebox.showinfo("Fin", "Match nul !")
            self.reset_game()
            return True
        return False

    def reset_game(self, _=None):
        self.board = [0] * 9
        self.current_player = 1
        for btn in self.buttons:
            btn.configure(text="", state="normal", fg_color="#2b2b2b")
        self.label_win.configure(text="Probabilité Victoire X : --%")
        self.label_draw.configure(text="Probabilité Match Nul : --%")


if __name__ == "__main__":
    app = MorpionApp()
    app.mainloop()