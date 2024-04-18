from app import db

class RevokedTokenModel(db.Model):
    _tablename_ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def init(self, jti):self.jti=jti