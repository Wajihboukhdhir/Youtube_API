from flask import Blueprint,request
from flask import json
from flask.json import jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_sqlalchemy import Pagination
import validators
from database import Bookmark,db
from constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask_jwt_extended import get_jwt_identity
from flasgger import Swagger,swag_from

bookmarks = Blueprint("bookmarks",__name__,url_prefix="/api/v1/bookmarks")

@bookmarks.route('/',methods=['POST','GET'])
@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/postbookmark.yml')

@jwt_required()
def deal_with_bookmarks():
        current_user=get_jwt_identity()
        if request.method == 'POST':

                
                body=request.get_json().get('body','')
                url = request.get_json().get('url','')
                
                if not validators.url(url):
                        return({
                                'ERROR':'Enter a Url that is VALID please !!'

                        }),HTTP_400_BAD_REQUEST
                if Bookmark.query.filter_by(url=url).first():
                        return jsonify({

                           'ERROR':'URL EXISTS'     
                        }),HTTP_409_CONFLICT
                bookmark=Bookmark(url=url,body=body,user_id=current_user)        
                db.session.add(bookmark)
                db.session.commit()

                return jsonify({
                  'id':bookmark.id,
                  'url':bookmark.url,
                  'short url':bookmark.short_url,
                  'number of visits':bookmark.visits,
                  'body':bookmark.body,
                  'created_at':bookmark.created_at,
                  'Updated_at':bookmark.updated_at

                }),HTTP_201_CREATED
        else:
                
                page = request.args.get('page',1,type=int)
                per_page = request.args.get('per_page',5,type=int)
                bookmarks=Bookmark.query.filter_by(
                        user_id=current_user).paginate(page=page,per_page=per_page)
                
                data=[]
                for bookmark in bookmarks.items:
                        data.append({
                  'id':bookmark.id,
                  'url':bookmark.url,
                  'short url':bookmark.short_url,
                  'number of visits':bookmark.visits,
                  'body':bookmark.body,
                  'created_at':bookmark.created_at,
                  'Updated_at':bookmark.updated_at
                        }) 
                meta={
                    "page":bookmarks.page,
                    "pages":bookmarks.pages,
                    "total": bookmarks.total,
                    "next":bookmarks.next_num,
                    "prev":bookmarks.prev_num,
                    "has_next":bookmarks.has_next,
                    "has_prev":bookmarks.has_prev,



                }        
                return jsonify({'DATA OF ALL BOOKMARKS':data,"META":meta}),HTTP_200_OK           





@bookmarks.delete("/<int:id>")
@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/delete.yml')

@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'ERROR': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({"SUCCESS":"Bookmark Succesfully deleted"}),HTTP_204_NO_CONTENT


@bookmarks.put('/<int:id>')
@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/put.yml')

@jwt_required()
def edit_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'ERROR': 'Item not found'}), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
        }), HTTP_400_BAD_REQUEST

    bookmark.url = url
    bookmark.body = body

    db.session.commit()

    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visit': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,
    }), HTTP_200_OK






   

