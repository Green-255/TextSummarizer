from db import db

class Summary(db.Model):
    __tablename__ = 'Summary_History'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(256))
    input_text = db.Column(db.Text, nullable=False)
    summary_type = db.Column(db.String(16), nullable=False)
    summary_text = db.Column(db.Text, nullable=False)
    # summary_length = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return f'<Summary {self.id} - {self.summary_type}>'