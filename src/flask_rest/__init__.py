import os
from flask_socketio import SocketIO
from flask import Flask, Blueprint
from flask_wtf.csrf import CSRFProtect
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

try:
    import settings

    project = Flask(
        settings.PROJECT_NAME,
        static_url_path=settings.STATIC,
        static_folder=settings.STATIC_PATH,
        root_path=settings.BASE_DIR
    )
    project.config.from_object(settings)
    db = MongoEngine(project)
    project.session_interface = MongoEngineSessionInterface(db)
    socketio = SocketIO(project)

    if settings.CSRF_ENABLED:
        CSRFProtect(project)

    for url_prefix, app_name in settings.APPS:
        app = Blueprint(
            app_name,
            app_name,
            url_prefix=url_prefix,
            template_folder=os.path.join(settings.BASE_DIR, "templates", app_name)
        )

        urls = __import__('%s.urls' % app_name, fromlist=[app_name])
        for args in urls.urls:
            url, view_func = args
            app.add_url_rule(url, view_func=view_func)

        project.register_blueprint(app)

except ImportError:
    pass
