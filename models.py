import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()


class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name_of_category = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    data_last_pars = db.Column(db.Integer)
    characteristics = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Category {self.name_of_category}>'
    

class TableCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    json_data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Category {self.id}>'