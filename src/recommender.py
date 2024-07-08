import time

from SteamGameRecommender.src.steam_handler import SteamHandler
import pandas as pd
import joblib
import asyncio


class Recommender:
    def __init__(self):
        print("Loading Recommender...")
        self.steam_handler = SteamHandler()
        self.current_recommender = None  # knn with cosine similarity
        self.expanded_tags = pd.read_csv('data/expanded_tags.csv')
        self.expanded_tags.index = self.expanded_tags['AppID']
        self.knn_cosine = joblib.load('models/tags.joblib')
        print("Loading Recommender finished...")

    async def recommend(self, steam_id, exclude_owned_games=True):
        """
        Function that:
        1)gets recommendation from some chosen model as steam game ids
        2)fetches steam game info from steam api
        3)returns response from steam api to frontend

        Parameters
        ----------
        steam_id - user Steam ID 64
        exclude_owned_games - whether to exclude already owned games on their steam account

        Returns
        -------
        Return response from steam api with all info about game

        """
        recommended_ids = set()

        # could be extended to other models
        if self.current_recommender is None:
            games = await self.steam_handler.get_recently_played_games(steam_id)
            for game in games:
                recommended_ids.update(self.knn_recommender(game['appid']))

        if exclude_owned_games:
            owned_games = await self.steam_handler.get_owned_games(steam_id, include_appinfo=False)
            owned_games_ids = set()
            for game in owned_games:
                owned_games.add(game['appid'])
            # exclude already owned games
            recommended_ids.difference_update(owned_games_ids)

        # get game info from steam api
        tasks = []
        for app_id in recommended_ids:
            tasks.append(self.steam_handler.get_app_info(app_id))
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        print(f'Took {end_time - start_time} seconds to get {len(results)} results')
        # return steam api response
        return results

    def knn_recommender(self, game_id, num_recommendations=5):
        """
        Simple recommender using KNN and cosine similarity. Cosine similarity as far as I know is better for sparse
        data.
        Just find vector of that game and find number of num_recommendation games using KNN

        Parameters
        ----------
        game_id - steam game id to
        num_recommendations - number of games to return

        Returns
        -------
        Steam game ids of the recommended games
        """
        query_vector = self.expanded_tags.loc[game_id].to_numpy()[1:].reshape(1, -1)
        distances, indices = self.knn_cosine.kneighbors(query_vector, n_neighbors=num_recommendations + 1)

        # Exclude the input game itself
        indices = indices[0][1:num_recommendations + 1]

        # Map indices back to AppIDs
        recommended_app_ids = self.expanded_tags.index[indices].tolist()

        return set(recommended_app_ids)

# async def main():
#    recommender = Recommender()
#    await recommender.recommend(76561198168015547)


# asyncio.run(main())

# expanded_tags = pd.read_csv('data/expanded_tags.csv')
# expanded_tags.index = expanded_tags['AppID']
# print(expanded_tags.columns)
# print("Current data shape:", expanded_tags.shape)
