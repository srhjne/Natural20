from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Monster(db.Model):

	__tablename__ = "monsters"


	monster_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(24), nullable=False)
	cr = db.Column(db.Float, nullable=False)


	def __repr__(self):
		return "<Monster id=%s, name=%s" % (self.monster_id, self.name)


class Attack(db.Model):

    __tablename__ = "attacks"

    attack_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    monster_id = db.Column(db.Integer, db.ForeignKey('monsters.monster_id'), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    damage_type = db.Column(db.String(24))
    avg_damage = db.Column(db.Integer, nullable=False)
    num_dice = db.Column(db.Integer)
    type_dice = db.Column(db.Integer)
    dice_modifier = db.Column(db.Integer)

    monster = db.relationship("Monster", backref="attack")

    def __repr__(self):
        return "<Attack id=%s, name=%s" % (self.attack_id, self.name)









def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///natural20'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."