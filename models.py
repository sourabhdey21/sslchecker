from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ssl_checks = db.relationship('SSLCheck', backref='user', lazy=True)

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

class SSLCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), nullable=False)
    check_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_valid = db.Column(db.Boolean, nullable=False)
    expiry_date = db.Column(db.DateTime)
    issuer = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'domain': self.domain,
            'check_date': self.check_date.isoformat(),
            'is_valid': self.is_valid,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'issuer': self.issuer
        } 