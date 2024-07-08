# SteamGameRecommender

![index](static/assets/index.png)

Simple recommendation model for Steam Users. It fetches recent played games for current user and gets the most similar 
games. User interacts with web page, model is running on server, which handles requests. For faster request time *asyncio* and
*aiohttp* were used


### Data for model
Data was acquired from [Steam 2024](https://www.kaggle.com/datasets/artermiloff/steam-games-dataset/code) and 
[Steam Store Data](https://www.kaggle.com/datasets/amanbarthwal/steam-store-data/data). Then simple EDA 
was done and multiple models were tested, including Simple KNN, KNN with TF-IDF, K-Means, DBScan. 
In the end KNN with cosine similarity was chosen as our model and our train data is in format:

| AppID | Action | Adventure | RPG  | Strategy | other tags... |
|-------|--------|-----------|------|----------|---------------|
| 001   | 3600   | 0         | 123  | 1233     | ...           |
| 002   | 0      | 0         | 0    | 0        | ...           |
| 003   | 123    | 0         | 1321 | 0        | ...           |

The features represent tags with associated "weights" indicating the extent to which a game belongs to each category. 
*Cosine similarity* was employed due to the sparsity of our data.


## Requirements
This project requires the following libraries to be installed:

- aiohttp
- flask
- joblib
- pandas

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary libraries.
```bash
pip install -r requirements.txt
```

## Usage

#### In order to try this web app, go to [steam web api](https://steamcommunity.com/dev/apikey) and get your own Steam Web API Key
1. Clone or download this repository to your local machine.
2. Create in SteamGameRecommender/src file **conf.py** and paste your API key there 
   * e.g API_KEY = 'some_api_key' 
3. Run the main script using the following command in your terminal:
```bash
python app.py
```
4. Access in your browser http://127.0.0.1:5000


## Example usage
![example](static/assets/example-usage.png)
