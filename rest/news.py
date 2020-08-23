from flask import (
    Blueprint, request, Response, jsonify
)
from external.news_api_client import newsapi
from models.news import NewsModel, NewsSchema
from models.ratings import RatingModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from models.recommend import RecommendModel

bp = Blueprint('news', __name__, url_prefix='/news')


@bp.route('/toplines', methods=(['GET']))
def toplines():
    page = request.args.get('page', default=1, type=int)
    result = newsapi.get_top_headlines(
        country="us", page=page)
    articles = [NewsModel(**article) for article in result["articles"]]
    NewsModel.bulk_save_to_db(articles)
    newsSchema = NewsSchema(many=True)
    return {
        "status": result["status"],
        "totalResults": result["totalResults"],
        "articles": [newsSchema.dump(articles)]
    }, 200


@bp.route('/<news_id>/like', methods=(['POST']))
@jwt_required
def like_news(news_id):
    user_id = get_jwt_identity()
    ratingModel = RatingModel(user_id, news_id, 1)
    # Ignore duplicate like request
    ratingModel.save_to_db()

    return Response(status=200)


@bp.route('/<news_id>/dislike', methods=(['POST']))
@jwt_required
def dislike_news(news_id):
    user_id = get_jwt_identity()
    ratingModel = RatingModel(user_id, news_id, -1)
    # Ignore duplicate disklike request
    ratingModel.save_to_db()
    return Response(status=200)


@bp.route('/recommend', methods=(['GET']))
@jwt_required
def recommend_news():
    user_id = get_jwt_identity()
    news_ids = RecommendModel.recommend_news_by_user_id(user_id)
    news = NewsModel.select_list_of_news(news_ids)
    newsSchema = NewsSchema(many=True)
    return {
        "news": newsSchema.dump(news)
    }, 200
