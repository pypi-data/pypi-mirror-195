from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine


class Database(SQLAlchemy):
	def connect(self, config, db_type):
		if db_type == 'postgre':
			url = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(**config)
		else:
			url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4'.format(**config)
		self.engine = create_engine(url)
		self.metadata = MetaData(bind=engine)

    def mount(self, app):
        super().init_app(app)


db = Database()
session = db.session