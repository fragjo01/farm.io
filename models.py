from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Item {self.name}>"
