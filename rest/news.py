from flask import (
    Blueprint, request, Response, jsonify
)
from external.news_api_client import newsapi
from models.news import NewsModel

bp = Blueprint('news', __name__, url_prefix='/news')


@bp.route('/<news_id>/like', methods=(['POST']))
def like_news(news_id):
    pass


@bp.route('/toplines', methods=(['GET']))
def toplines():
    page = request.args.get('page', default=1, type=int)
    result = newsapi.get_top_headlines(
        country="us", page=page)
    articles = [NewsModel(**article) for article in result["articles"]]
    NewsModel.bulk_save_to_db(articles)
    return result, 200
