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
        steam_input = request.form['steam_id']
        print(f'Got steam input: {steam_input}')

        # Check if the input is a vanity URL and convert it to SteamID64
        if steam_input.isdigit():  # Check if input is already a SteamID64
            steam_id = steam_input
        else:  # Assume it's a vanity URL, resolve it to SteamID64
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            steam_id = loop.run_until_complete(recommender.steam_handler.get_steam_id64(steam_input))

        print(f'Resolved Steam ID: {steam_id}')

        # Now you have the SteamID64, proceed with recommendation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        recommended_games = loop.run_until_complete(recommender.recommend(steam_id))

        return jsonify(recommended_games)

    except KeyError:
        return jsonify({'error': 'Steam ID or Vanity URL not provided in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
