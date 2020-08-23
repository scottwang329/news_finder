from db import db
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.dialects import postgresql
from sqlalchemy import create_engine
from models.ratings import RatingModel


def generate_recommend_table(ctx):

    ctx.push()

    # Read news rating data from Rating table
    rating_df = pd.read_sql(
        db.session.query(RatingModel).statement,
        db.session.bind
    )

    n_users = rating_df.user_id.nunique()
    n_items = rating_df.news_id.nunique()

    # Construct user-item rating table for calculation
    final = pd.pivot_table(rating_df, values='rating',
                           index='user_id', columns='news_id')

    # Calculate cosine similarities for users and items.
    user_similarity = cosine_similarity(final.fillna(0))
    item_similarity = cosine_similarity(final.fillna(0).T)
    top_k_users = np.argsort(user_similarity[1, :])[-2:-10-1:-1]
    top_k_items = np.argsort(item_similarity[1, :])[-2:-10-1:-1]

    # Fill the empty field with average value
    final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)
    final_item = final.fillna(final.mean(axis=0))

    # Algorithms for collabrative filtering, using the top 10 users and items
    def predict_user(ratings, similarity, k=10):
        pred = np.zeros((n_users, n_items))
        for i in range(n_users):
            top_k_users = np.argsort(similarity[i, :])[-2:-k-1:-1]
            denominator = np.sum(np.abs(similarity[i, top_k_users]))
            if denominator != 0:
                ratings_mean = ratings[top_k_users, :].mean()
                pred[i, :] = similarity[i, top_k_users].dot(
                    ratings[top_k_users, :] - ratings_mean)
                pred[i, :] /= denominator
                pred[i, :] += ratings_mean
        return pred

    def predict_item(ratings, similarity, k=10):
        pred = np.zeros((n_users, n_items))
        for i in range(n_items):
            top_k_items = np.argsort(similarity[i, :])[-2:-k-1:-1]
            denominator = np.sum(np.abs(similarity[i, top_k_items]))
            if denominator != 0:
                pred[:, i] = ratings[:, top_k_items].dot(
                    similarity[i, top_k_items])
                pred[:, i] /= denominator
        return pred

    # Predict the rating
    item_prediction = predict_item(final_item.to_numpy(), item_similarity)
    user_prediction = predict_user(final_user.to_numpy(), user_similarity)

    # Combine user-based CF and item-based CF, and replace the original rating as NAN
    recommend_matrix = user_prediction/2 + item_prediction/2
    recommend_matrix[~np.isnan(final.to_numpy())] = -float("NaN")

    # Write the final value into Database
    recommend_df = pd.DataFrame(
        index=final.index,
        columns=['news_ids']
    )
    recommend_df['news_ids'] = [
        array for array in final.columns.values[np.argsort(-recommend_matrix, axis=1)[:, :10]]]

    recommend_df.to_sql('recommend', con=db.session.bind, if_exists='replace',
                        dtype={"user_id": postgresql.VARCHAR,
                               "news_ids": postgresql.ARRAY(postgresql.VARCHAR)})
