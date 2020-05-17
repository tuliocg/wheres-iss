import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app, db
from config import config

enviroment = os.environ.get('APP_SETTINGS')
app.config.from_object(config[enviroment])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
