from flask import _app_ctx_stack, current_app
import pymysql
import pymysql.cursors

class MySQL(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MYSQL_HOST', 'localhost')
        app.config.setdefault('MYSQL_USER', None)
        app.config.setdefault('MYSQL_PASSWORD', None)
        app.config.setdefault('MYSQL_DB', None)
        app.config.setdefault('MYSQL_PORT', 3306)
        app.config.setdefault('MYSQL_CHARSET', 'utf8mb4')
        app.config.setdefault('MYSQL_CURSORCLASS', pymysql.cursors.DictCursor)
        
        # Use the teardown_appcontext to close the database connection
        app.teardown_appcontext(self.teardown)

    def connect(self):
        config = current_app.config
        
        # Get cursor class
        cursorclass = config['MYSQL_CURSORCLASS']
        if isinstance(cursorclass, str):
            # If it's a string, try to get the actual class
            if cursorclass == 'DictCursor':
                cursorclass = pymysql.cursors.DictCursor
            elif cursorclass == 'SSCursor':
                cursorclass = pymysql.cursors.SSCursor
            elif cursorclass == 'SSDictCursor':
                cursorclass = pymysql.cursors.SSDictCursor
            else:
                cursorclass = pymysql.cursors.Cursor
        
        # Create connection
        return pymysql.connect(
            host=config['MYSQL_HOST'],
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DB'],
            port=config['MYSQL_PORT'],
            charset=config['MYSQL_CHARSET'],
            cursorclass=cursorclass
        )

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'pymysql_db'):
            ctx.pymysql_db.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'pymysql_db'):
                ctx.pymysql_db = self.connect()
            return ctx.pymysql_db