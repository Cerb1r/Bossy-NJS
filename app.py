from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Charger les modèles entraînés à l'étape 3
model_wins = joblib.load('models/best_model_wins.pkl')
model_draw = joblib.load('models/best_model_draw.pkl')


def encode_board(board):
    # Transforme [0, 1, -1] en 18 colonnes binaires (ci_x, ci_o)
    encoded = []
    for cell in board:
        encoded.append(1 if cell == 1 else 0)  # x
        encoded.append(1 if cell == -1 else 0)  # o
    return np.array(encoded).reshape(1, -1)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    board = data['board']  # ex: [1, 0, -1, 0, 0, ...]

    encoded_board = encode_board(board)

    # Probabilité que X gagne à partir de cette position
    prob_win = model_wins.predict_proba(encoded_board)[0][1]
    # Probabilité de match nul
    prob_draw = model_draw.predict_proba(encoded_board)[0][1]

    return jsonify({
        'prob_win': float(prob_win),
        'prob_draw': float(prob_draw)
    })


if __name__ == '__main__':
    app.run(port=5000)

