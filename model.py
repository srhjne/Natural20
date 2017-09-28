from flask_sqlalchemy import SQLAlchemy
import datetime


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

    def get_suitable_monsters(self):
        monsters = Monster.query.filter(Monster.cr >= self.min_cr, Monster.cr <=self.max_cr).all()
        return monsters



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


    def get_damage(self):
        if self.num_dice:
            damage_val = self.num_dice*random.randint(1,self.type_dice)
            if self.dice_modifier:
                damage_val += self.dice_modifier
        else:
            damage_val = avg_damage
        return damage_val



#Classes for handling users: User, Goal, GoalStatus, UserStatus

class User(db.Model):

    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(32), nullable=False)



    def __repr__(self):
        return "<User id=%s, username=%s>" %(self.user_id, self.username)

    def get_current_status(self):
        return self.userstatus[-1]


    def get_current_goals(self):
        goals = Goal.query.filter(Goal.user_id == self.user_id, Goal.valid_from < datetime.datetime.now(), Goal.valid_to > datetime.datetime.now()).all()
        return goals

    def get_unresolved_goals(self):
        goals = Goal.query.filter(Goal.user_id == self.user_id, Goal.valid_from < datetime.datetime.now(), Goal.resolved.is_(None)).all()
        return goals

    def get_unresolved_overdue_goals(self):
        goals = Goal.query.filter(Goal.user_id == self.user_id, Goal.valid_to < datetime.datetime.now(), Goal.resolved.is_(None)).all()
        return goals

    def calc_xp(self, goal_value, valid_from, valid_to, goal_type="Steps"):
        timedelta = (valid_to - valid_from).total_seconds()
        scaled_value_test = goal_value/timedelta

        xp = 500

        goals = Goal.query.filter(Goal.goal_type == goal_type, Goal.user_id==self.user_id).all()
        if not goals:
            xp = 500
        else:
            for goal in goals:
                timedelta = (goal.valid_to - goal.valid_from).total_seconds()
                scaled_value = goal.value/timedelta
                ratio = scaled_value_test/scaled_value
                if ratio < 0.8:
                    xp = 200
                    break
                elif ratio >= 0.8 and ratio < 1.1:
                    xp = 300
        return xp

    @staticmethod
    def get_level_from_xp(xp):
        level = LevelLookup.query.filter(LevelLookup.required_xp <= xp).order_by(LevelLookup.level).all()
        return level[-1]

    @classmethod
    def make_new_user(cls, username, email, password):
        user = cls(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        user_db = cls.query.filter(cls.username==username).first()
        userstatus = UserStatus(user_id=user_db.user_id,current_hp=12,current_xp=0,
                                level=1,date_recorded=datetime.datetime.now())
        db.session.add(userstatus)
        db.session.commit()

    def reroll_stats(self):
        userstatus = UserStatus(user_id=self.user_id, current_xp=0, current_hp=12, level=1, date_recorded=datetime.datetime.now())
        db.session.add(userstatus)
        db.session.commit()

class Goal(db.Model):

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    goal_type = db.Column(db.String(20), nullable=False)
    valid_from = db.Column(db.TIMESTAMP, nullable=False)
    valid_to = db.Column(db.TIMESTAMP, nullable=True)
    value = db.Column(db.Integer, nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    resolved = db.Column(db.String(1), nullable=True)

    user = db.relationship("User", backref=db.backref("goal", order_by=valid_to))

    
    def __repr__(self):
        return "<Goal id=%s type=%s value=%s>"%(self.goal_id, self.goal_type, self.value)


    def get_current_status(self):
        return self.goalstatus[-1]

    def get_status_series(self):
        statuses = sorted([(status.date_recorded, status.value) for status in self.goalstatus])
        return statuses

    def commit_goal(self):
        db.session.add(self)
        db.session.commit()

    def make_goal_info_dictionary(self):
        return {"username": self.user.username,"achieved": True, "goal_type": self.goal_type, "goal_value" : self.value,
                              "valid_from": self.valid_from, "valid_to" : self.valid_to,
                              "goal_id": self.goal_id, "xp": self.xp, "current_xp": self.user.get_current_status().current_xp,
                              "current_level": self.user.get_current_status().level}
    

class GoalStatus(db.Model):

    __tablename__ = "goalstatuses"

    goalstatus_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.goal_id"), nullable=False)
    date_recorded = db.Column(db.TIMESTAMP, nullable=False)
    value = db.Column(db.Integer,nullable=False)

    goalstatus = db.relationship("Goal", backref=db.backref("goalstatus", order_by=date_recorded))


    def __repr__(self):
        return "<Goal Status id=%s, date=%s>"%(self.goalstatus_id, self.date_recorded)

    @classmethod
    def make_first_status(cls, goal_type, valid_from, valid_to, goal_value, xp, user_id):
        goal_db = Goal.query.filter(Goal.user_id==user_id, Goal.xp==xp, Goal.goal_type==goal_type, Goal.value==goal_value, Goal.valid_from==valid_from, Goal.valid_to==valid_to).first()
        gs = cls(goal_id=goal_db.goal_id,value=0,date_recorded=valid_from)
        db.session.add(gs)
        db.session.commit()


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

    @classmethod
    def create_save_updated_status(cls, user, current_status, new_xp, new_hp):
        new_level = user.get_level_from_xp(new_xp)
        if new_level.level > current_status.level:
            new_hp = new_level.hit_point_max
        else:
            new_hp = max(0, new_hp)
        new_status = cls(user_id=user.user_id, current_xp = new_xp, current_hp=new_hp, level=new_level.level, 
                            date_recorded=datetime.datetime.now())  
        db.session.add(new_status)
        db.session.commit()






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