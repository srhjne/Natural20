from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


# Classes for DnD mechanics: LevelLookup, Monster, Attack
class LevelLookup(db.Model):

    __tablename__ = "levellookup"

    level = db.Column(db.Integer, primary_key=True)
    min_cr = db.Column(db.Float)
    max_cr = db.Column(db.Float)
    required_xp = db.Column(db.Integer)
    hit_point_max = db.Column(db.Integer)

    def __repr__(self):
        return "<Level %s>"%self.level



class Monster(db.Model):

	__tablename__ = "monsters"


	monster_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(32), nullable=False)
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

    monster = db.relationship("Monster", backref=db.backref("attack"))

    def __repr__(self):
        return "<Attack id=%s, name=%s" % (self.attack_id, self.name)


#Classes for handling users: User, Goal, GoalStatus, UserStatus

class User(db.Model):

    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(32), nullable=False)



    def __repr__(self):
        return "<User id=%s, username=%s>" %(self.user_id, self.username)

class Goal(db.Model):

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    goal_type = db.Column(db.String(20), nullable=False)
    valid_from = db.Column(db.TIMESTAMP, nullable=False)
    valid_to = db.Column(db.TIMESTAMP, nullable=True)
    value = db.Column(db.Integer, nullable=False)
    xp = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", backref=db.backref("goal", order_by=valid_to))

    
    def __repr__(self):
        return "<Goal id=%s type=%s value=%s>"%(self.goal_id, self.goal_type, self.value)


class GoalStatus(db.Model):

    __tablename__ = "goalstatuses"

    goalstatus_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"), nullable=False)
    date_recorded = db.Column(db.TIMESTAMP, nullable=False)
    value = db.Column(db.Integer,nullable=False)

    goalstatus = db.relationship("Goal", backref=db.backref("goalstatus", order_by=date_recorded))


    def __repr__(self):
        return "<Goal Status id=%s, date=%s>"%(self.goalstatus_id, self.date_recorded)


class  UserStatus(db.Model):

    __tablename__ = "userstatuses"

    userstatus_id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    level = db.Column(db.Integer, db.ForeignKey("levellookup.level"), nullable=False)
    current_xp = db.Column(db.Integer,nullable=False)
    current_hp = db.Column(db.Integer, nullable=False)
    date_recorded = db.Column(db.TIMESTAMP, nullable=False)

    user = db.relationship("User", backref=db.backref("userstatus", order_by = date_recorded))

    levellookup = db.relationship("LevelLookup", backref=db.backref("userstatus"))

    def __repr__(self):
        return "<User Status id=%s, user id=%s, date=%s"%(self.userstatus_id,self.user_id,self.date_recorded)









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