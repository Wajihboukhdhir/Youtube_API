from flask import Blueprint,request
from flask import json
from flask.json import jsonify
from flask_jwt_extended.view_decorators import jwt_required
from flask_sqlalchemy import Pagination
import validators
from src.database import Youtube,db,Singer
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask_jwt_extended import get_jwt_identity
from flasgger import Swagger,swag_from

youtubes = Blueprint("youtubes",__name__,url_prefix="/api/v1/youtubes")

@youtubes.route('/',methods=['POST','GET'])
@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/postyoutube.yml')

@jwt_required()
def deal_with_youtubes():
        current_user=get_jwt_identity()
        if request.method == 'POST':
                


                body=request.get_json().get('body','')
                url = request.get_json().get('url','')

                if not validators.url(url):
                        return({
                                'ERROR':'Enter a Url that is VALID please !!'

                        }),HTTP_400_BAD_REQUEST
                if not ('youtube' in url):
                        return({
                                'ERROR':'Enter a Url that is a youtube link !!'

                        }),HTTP_400_BAD_REQUEST

                if Youtube.query.filter_by(url=url,user_id=current_user).first():
                        return jsonify({

                           'ERROR':'URL EXISTS'     
                        }),HTTP_409_CONFLICT
                youtube=Youtube(url=url,body=body,user_id=current_user) 
                singer = Singer(body=body,user_id=current_user)
                     
                db.session.add(youtube)
                db.session.commit()
                singer1=Singer.query.filter_by(body=body).first()

                if singer1:
                    singer1.songs=singer1.songs + 1
                    db.session.commit()
                else:        
                    db.session.add(singer)  
                    db.session.commit()
                
                return jsonify({
                  'id':youtube.id,
                  'url':youtube.url,
                  'short url':youtube.short_url,
                  'Downloads':youtube.visits,
                  'body':youtube.body,
                  'created_at':youtube.created_at,
                  'Updated_at':youtube.updated_at,
                  'userID':youtube.user_id

                }),HTTP_201_CREATED
        else:
                
                page = request.args.get('page',1,type=int)
                per_page = request.args.get('per_page',10,type=int)
                youtubes=Youtube.query.filter_by(
                        user_id=current_user).paginate(page=page,per_page=per_page)
                
                data=[]
                for youtube in youtubes.items:
                        data.append({
                  'id':youtube.id,
                  'url':youtube.url,
                  'short url':youtube.short_url,
                  'downloads':youtube.visits,
                  'body':youtube.body,
                  'created_at':youtube.created_at,
                  'Updated_at':youtube.updated_at,
                  'userID':youtube.user_id
                        }) 
                meta={
                    "page":youtubes.page,
                    "pages":youtubes.pages,
                    "total": youtubes.total,
                    "next":youtubes.next_num,
                    "prev":youtubes.prev_num,
                    "has_next":youtubes.has_next,
                    "has_prev":youtubes.has_prev,



                }        
                return jsonify({'DATA OF ALL youtube videos':data,"META":meta}),HTTP_200_OK           





@youtubes.delete("/<int:id>")
@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/deleteyoutube.yml')

@jwt_required()
def delete_youtube(id):
    current_user = get_jwt_identity()

    youtube = Youtube.query.filter_by(user_id=current_user, id=id).first()

    if not youtube:
        return jsonify({'ERROR': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(youtube)
    db.session.commit()
    return jsonify({"SUCCESS":"Youtube Succesfully deleted"}),HTTP_204_NO_CONTENT


@youtubes.put('/<int:id>')
@youtubes.patch('/<int:id>')
@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/putyoutube.yml')

@jwt_required()
def edit_youtube(id):
    current_user = get_jwt_identity()

    youtube = Youtube.query.filter_by(user_id=current_user, id=id).first()

    if not youtube:
        return jsonify({'ERROR': 'Item not found'}), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid url'
        }), HTTP_400_BAD_REQUEST
    if not ('youtube' in url):
                        return({
                                'ERROR':'Enter a Url that is a youtube link !!'

                        }),HTTP_400_BAD_REQUEST
   

    youtube.url = url
    youtube.body = body

    db.session.commit()

    return jsonify({
        'id': youtube.id,
        'url': youtube.url,
        'short_url': youtube.short_url,
        'downloads': youtube.visits,
        'body': youtube.body,
        'created_at': youtube.created_at,
        'updated_at': youtube.updated_at,
    }), HTTP_200_OK

@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/getbyID.yml')
@youtubes.get("/<int:id>")
@jwt_required()
def get_Specific_Youtube(id):
        current_user=get_jwt_identity()

        youtube= Youtube.query.filter_by(user_id=current_user,id=id).first()

        if not youtube:

                return jsonify({"message error":"item not found Sorry"}),HTTP_404_NOT_FOUND
        
        return jsonify({
          'id':youtube.id,
                  'url':youtube.url,
                  'short url':youtube.short_url,
                  'number of downloads':youtube.visits,
                  'body':youtube.body,
                  'created_at':youtube.created_at,
                  'Updated_at':youtube.updated_at

        }),HTTP_200_OK

@youtubes.get("/stats")
@swag_from('C:/Users/Leila/Desktop/bookmarksrestapi/src/docs/auth/stats.yaml')


@jwt_required()
def statistics():
        current_user = get_jwt_identity()
        data=[]
        items=Youtube.query.filter_by(user_id=current_user).all()

        for i in items:
                new_link={
               'name':i.body,         
               'URL':i.url,
               'Downloads':i.visits
               
               


                } 
                data.append(new_link)

        return jsonify({'data':data}),HTTP_200_OK


@youtubes.get("/singers")
@swag_from('./docs/Singers.yaml')


@jwt_required()
def singers():
        current_user = get_jwt_identity()
        data=[]
        items=Singer.query.filter_by().all()

        for i in items:
                new_link={
               'name of the singer':i.body,         
               'number of songs':i.songs,
               
               
               


                } 
                data.append(new_link)

        return jsonify({'data':data}),HTTP_200_OK





   

