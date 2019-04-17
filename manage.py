import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
import app.models

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
