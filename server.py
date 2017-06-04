from flask import Flask, render_template, request, abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# data base models
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String)
    signature = db.Column(db.String)
    body = db.Column(db.String)
    publish_date = db.Column(db.String)
    article_url = db.Column(db.String)

    def __repr__(self):
        return '<Article %r' % self.article_url


@app.route('/')
def form_page():
    signature = request.cookies.get('user_signature', 'Anonymous')
    return render_template('article.html', user_signature=signature, article=None)


@app.route('/article', methods=['POST'])
def handle_article_data():
    publish_date = datetime.datetime.now().strftime('%d-%B-%Y')
    header = request.form.get('form-header')
    signature = request.form.get('form-signature')
    body = request.form.get('form-body')
    article_url = '%s-%s' % (header.replace(' ', '-'), publish_date)

    new_article = Article(header=header, signature=signature, body=body,
                          publish_date=publish_date, article_url=article_url)

    db.session.add(new_article)
    db.session.commit()

    article_info_json = jsonify({
        'article_url': article_url,
        'header': header,
        'signature': signature,
        'publish_date': publish_date,
        'body': body,
    })

    response = make_response(article_info_json)
    response.set_cookie('user_signature', signature)
    return response

# post запрос на edit у статьи остаётся ёё исходный урл, а остальное меняется


@app.route("/<url>")
def article_page(url):
    article = Article.query.filter_by(article_url=url).first()
    if article is None:
        return abort(404)
    user_signature = request.cookies.get('user_signature', None)
    if user_signature is None:
        user_signature = 'Anonymous'
    author = True if user_signature == article.signature else False
    return render_template('article.html', article=article, author=author)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=5050)
