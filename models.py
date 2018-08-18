from app import db

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key = True)
    student = db.Column(db.String(20))
    teacher = db.Column(db.String(20))
    subject = db.Column(db.String(20))
    address = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    payment_type = db.Column(db.String(5))
    status = db.Column(db.String(10))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {'id': self.id,
                'student': self.student,
                'teacher': self.teacher,
                'subject': self.subject,
                'address': self.address,
                'duration': self.duration,
                'payment_type': self.payment_type,
                'status': self.status}

    def __str__(self):
        return '{} - {} - {}'.format(str(self.id), self.student, self.teacher)
