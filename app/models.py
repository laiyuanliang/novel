from . import db

class Fiction(db.Model):
    __tablename__ = "fiction"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    fic_name = db.Column(db.String(30), nullable=False)
    fic_id = db.Column(db.String(15), nullable=False)
    fic_img = db.Column(db.String(100))
    fic_comment = db.Column(db.String(255))
    fic_source_url = db.Column(db.String(100), nullable=False)
    new_content = db.Column(db.String(50))
    new_url = db.Column(db.String(15))
    update_time = db.Column(db.String(80))

class Fiction_Lst(db.Model):
    __tablename__ = "fiction_lst"
    id = db.Column(db.Integer, primary_key=True)
    fic_id = db.Column(db.String(15), nullable=False)
    chapter_id = db.Column(db.String(15), nullable=False)
    chapter_name = db.Column(db.String(50))
    chapter_source_url = db.Column(db.String(100), nullable=False)

class Fiction_Content(db.Model):
    __tablename__ = "fiction_content"
    id = db.Column(db.Integer, primary_key=True)
    fic_id = db.Column(db.String(15), nullable=False)
    chapter_id = db.Column(db.String(15), nullable=False)
    chapter_content = db.Column(db.Text, nullable=False) 
