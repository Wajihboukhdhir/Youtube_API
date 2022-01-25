from flask import Flask, jsonify,redirect
import os
from src.constants.http_status_codes import HTTP_200_OK, HTTP_226_IM_USED, HTTP_302_FOUND, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask_jwt_extended import JWTManager
from src.auth import auth
from src.bookmarks import bookmarks
from src.youtube import youtubes

from src.database import db,Bookmark,Youtube
from flasgger import Swagger,swag_from
from src.config.swagger import template,swagger_config
def create_app(test_config=None): 
      app = Flask(__name__,instance_relative_config=True)
      app.config['JSON_SORT_KEYS'] = False
      if test_config is None:
       app.config.from_mapping(
              SECRET_KEY=os.environ.get
              ("SECRET_KEY"),
              SQLALCHEMY_DATABASE_URI='postgresql://postgres:root@localhost/bookmarks',
              SQLALCHEMY_TRACK_MODIFICATIONS=False,
              JWT_SECRET_KEY='JWT_SECRET_KEY',
              
              ) 
       app.config["SWAGGER"]={
                    'title':"API FOR MANAGING YOUTUBE SONGS",
                    'uiversion':2
              }
      else:
       app.config.from_mapping(test_config) 
      
      
      db.app=app
      db.init_app(app)
      JWTManager(app)
      app.register_blueprint(auth)
      app.register_blueprint(bookmarks)
      app.register_blueprint(youtubes)
      
      swagger = Swagger(app,config=swagger_config,template=template)


      @app.get('/<short_url>')
      @swag_from('./docs/short_url.yml')
      def redirection(short_url):
            youtube=Youtube.query.filter_by(short_url=short_url).first_or_404()

            if youtube:              
                  return redirect(youtube.url)



      
      
      




      @app.get('/youtube/<short_url>')
      @swag_from('./docs/short_urlyoutube.yml')

      def redirection1(short_url):
            youtube=Youtube.query.filter_by(short_url=short_url).first_or_404()

            if youtube.visits==0:
                  youtube.visits=youtube.visits+1
                  db.session.commit()
                  
                  theurl=youtube.url
                  index = theurl.find('youtube')
                  final_string = theurl[:index] + 'ss' + theurl[index:]

                  return redirect(final_string) 
            else :
                  return "You Have Downloaded this song Already!"             


      
      @app.errorhandler(HTTP_404_NOT_FOUND)
      def handler_notfound(e):
            
             return jsonify({"ERROR":"NOT FOUND!!"}),HTTP_404_NOT_FOUND
      
      # 500 error to ensure that we have to be working in development not production mode
      @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
      def handler_internal_server_error(e):
            return jsonify({"ERROR":"INTERNAL SERVER ERROR!!"}),HTTP_500_INTERNAL_SERVER_ERROR
      
      return app

