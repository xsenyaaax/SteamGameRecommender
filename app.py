from flask import Flask, request, jsonify, render_template
import asyncio
from SteamGameRecommender.src.recommender import Recommender

app = Flask(__name__)
recommender = Recommender()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        steam_id = request.form['steam_id']
        print(f'Got steam id {steam_id}')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        recommended_games = loop.run_until_complete(recommender.recommend(steam_id))
        return jsonify(recommended_games)
    except KeyError:
        return jsonify({'error': 'Steam ID not provided in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
