template = {
    "swagger": "2.0",
    "info": {
        "title": "API for Youtube Songs & Services",
        "description": "API for Managing Youtube Songs (and Their Singers) and favorite Links",
        "contact": {
            "TBS": "",
            "Wajih Boukhdhir": "",
            "email": "wajih.boukhdhir@gmail.com",
            "url": "www.API_FLASK_Wajih_Boukhdhir.com",
        },
        "termsOfService": "www.TBS_WEB.com/",
        "version": "1.0"
    },
    "basePath": "/api/v1",  
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}