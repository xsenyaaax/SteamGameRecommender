import time

from SteamGameRecommender.src.steam_handler import SteamHandler
import pandas as pd
import joblib
import asyncio


class Recommender:
    def __init__(self):
        self.steam_handler = SteamHandler()
        self.current_recommender = None  # knn with cosine similarity
        self.expanded_tags = pd.read_csv('data/expanded_tags.csv')
        self.expanded_tags.index = self.expanded_tags['AppID']
        self.knn_cosine = joblib.load('models/tags.joblib')

    async def recommend(self, steam_id):
        if self.current_recommender is None:
            games = await self.steam_handler.get_recently_played_games(steam_id)
            recommended_ids = set()
            for game in games:
                recommended_ids.update(self.knn_recommender(game['appid']))

        tasks = []
        for app_id in recommended_ids:
            tasks.append(self.steam_handler.get_app_info(app_id))
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        print(f'Took {end_time - start_time} seconds to get {len(results)} results')
        return results



    def knn_recommender(self, game_id, num_recommendations=5):
        query_vector = self.expanded_tags.loc[game_id].to_numpy()[1:].reshape(1, -1)
        distances, indices = self.knn_cosine.kneighbors(query_vector, n_neighbors=num_recommendations + 1)

        # Exclude the input game itself
        indices = indices[0][1:num_recommendations + 1]

        # Map indices back to AppIDs
        recommended_app_ids = self.expanded_tags.index[indices].tolist()

        return set(recommended_app_ids)
        # Return the top 5 most similar games along with their tags
        # return self.expanded_tags.loc[recommended_app_ids]


#async def main():
#    recommender = Recommender()
#    await recommender.recommend(76561198168015547)


#asyncio.run(main())

# expanded_tags = pd.read_csv('data/expanded_tags.csv')
# expanded_tags.index = expanded_tags['AppID']
# print(expanded_tags.columns)
# print("Current data shape:", expanded_tags.shape)
