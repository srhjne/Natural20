from flask_sqlalchemy import SQLAlchemy
import datetime
import random



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

    def calc_xp(self, goal_value, valid_from, valid_to, goal_type="Steps", frequency="Total"):
        timedelta = (valid_to - valid_from).total_seconds()
        if frequency == "Daily":
            days = timedelta/(24*60*60)
            goal_value = goal_value*days
        
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


    def update_setting(self, password=False, email=False):
        if password:
            self.password = password
        if email:
            self.email = email
        db.session.commit()

    def get_current_sleep_goals(self):
        return [goal for goal in self.goal if goal.goal_type=="Sleep" and not goal.resolved and goal.valid_to > datetime.datetime.now()]
    
    def get_friend_requests(self):
        return db.session.query(Friendship, User).join(User, User.user_id == Friendship.user_id_1).filter(Friendship.user_id_2 == self.user_id, Friendship.verified == False).all()


    def get_sent_friend_requests(self):
        return db.session.query(Friendship, User).join(User, User.user_id == Friendship.user_id_2).filter(Friendship.user_id_1 == self.user_id, Friendship.verified == False).all()

    def get_friends(self):
        first_list = db.session.query(User, Friendship.user_id_2).join(Friendship, User.user_id == Friendship.user_id_1)
        new_list1 = first_list.filter((Friendship.user_id_2 == self.user_id), Friendship.verified==True).all()
        second_list = db.session.query(User, Friendship.user_id_1).join(Friendship, User.user_id == Friendship.user_id_2)
        new_list2 = second_list.filter((Friendship.user_id_1 == self.user_id), Friendship.verified==True).all()
        new_list1.extend(new_list2)
        return new_list1


    def check_friendship(self, friend_id):
        friend_id_list = [friend.user_id for friend, user_id in self.get_friends()]
        return friend_id in friend_id_list

    def check_pending_friend_request(self, friend_id):
        print self.get_sent_friend_requests()
        friend_request_list =[friend.user_id for (friendship, friend) in self.get_sent_friend_requests()]
        print friend_id, friend_request_list, friend_id in friend_request_list
        return friend_id in friend_request_list

    def get_current_team(self):
        teams = [userteam.team for userteam in self.userteam if userteam.valid_from < datetime.datetime.now() and userteam.valid_to > datetime.datetime.now()]
        if teams:
            return teams[0]
        else:
            return None

    def leave_current_team(self):
        current_userteam = [userteam for userteam in self.userteam if userteam.valid_from < datetime.datetime.now() and userteam.valid_to > datetime.datetime.now()]
        if len(current_userteam) > 1 or not current_userteam:
            print "oh no team is not working properly", current_userteam
            return False
        else:
            current_userteam[0].valid_to = datetime.datetime.now()
            print current_userteam[0].team
            print current_userteam[0].team.teamname
            return current_userteam[0].team.teamname



class Goal(db.Model):

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    goal_type = db.Column(db.String(20), nullable=False)
    valid_from = db.Column(db.TIMESTAMP, nullable=False)
    valid_to = db.Column(db.TIMESTAMP, nullable=True)
    value = db.Column(db.Integer, nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.String(7), nullable=True)
    resolved = db.Column(db.String(1), nullable=True)

    user = db.relationship("User", backref=db.backref("goal", order_by=valid_to))

    
    def __repr__(self):
        return "<Goal id=%s type=%s value=%s>"%(self.goal_id, self.goal_type, self.value)


    def get_current_status(self):
        return self.goalstatus[-1]

    def get_status_last_3days(self):
        statuses = [status for status in self.goalstatus if (datetime.datetime.now() - status.date_recorded).total_seconds() < 60*60*24*3.0]
        return statuses

    def get_status_series(self):
        statuses = sorted([{"date_recorded":status.date_recorded, "value":status.value} for status in self.goalstatus])
        return statuses

    def get_daily_status_series(self):
        status_series = {}
        for status in self.goalstatus:
            day_recorded = status.date_recorded.strftime("%Y-%m-%d")
            status_series[day_recorded] = {"value": status.value, "date_recorded": status.date_recorded}
            if self.goal_type == "Sleep":
                status_series[day_recorded]["bedtime"] = status.sleepstatus[0].bedtime.strftime("%H:%M")
                status_series[day_recorded]["waketime"] = status.sleepstatus[0].waketime.strftime("%H:%M")
        return status_series

    def get_mean_value_daily(self):
        daily_progress = self.get_daily_status_series()
        daily_values = [daily_progress[status]['value'] for status in daily_progress]
        return sum(daily_values)/float(len(daily_values))


    def commit_goal(self):
        db.session.add(self)
        db.session.commit()

    def make_goal_info_dictionary(self):
        return {"username": self.user.username, "goal_type": self.goal_type, "goal_value" : self.value,
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


class SleepStatus(db.Model):

    __tablename__ = "sleepstatuses"

    goalstatus_id = db.Column(db.Integer, db.ForeignKey("goalstatuses.goalstatus_id"), primary_key=True)
    bedtime = db.Column(db.TIMESTAMP, nullable=False)
    waketime = db.Column(db.TIMESTAMP, nullable=False)



    goalstatus = db.relationship('GoalStatus', backref=db.backref("sleepstatus"))

    def __repr__(self):
        return "<Sleep status id=%s, bedtime=%s, waketime=%s"%(goalstatus_id,bedtime.strftime("%H:%M"), waketime.strftime("%H:%M"))

    @classmethod
    def save_sleep_goal_status(cls, goal ,bedtime, waketime, frequency="Total", date_recorded=None, first=False):
        sleep_seconds, bedtime, waketime = cls.get_sleep_time_from_strings(bedtime,waketime)
        
        if not date_recorded:
            date_recorded=datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"),"%Y-%m-%d")
        if frequency != "Daily" and not first:
            most_recent_status = goal.get_current_status()
            value = most_recent_status.value+sleep_seconds
        else:
            value = sleep_seconds
        gs = GoalStatus(goal_id=goal.goal_id, date_recorded=date_recorded, value=value)
        db.session.add(gs)
        db.session.commit()
        gs = GoalStatus.query.filter(GoalStatus.goal_id==goal.goal_id, GoalStatus.date_recorded==date_recorded, GoalStatus.value==value).first()
        ss = cls(goalstatus_id = gs.goalstatus_id, bedtime=bedtime, waketime=waketime)
        db.session.add(ss)
        db.session.commit()

    @staticmethod
    def get_sleep_time_from_strings(bedtime, waketime):
        bedtime = datetime.datetime.strptime(bedtime, "%H:%M")
        waketime = datetime.datetime.strptime(waketime, "%H:%M")
        delta = bedtime - waketime
        sleep_seconds = 24*60*60 - delta.total_seconds()
        return sleep_seconds, bedtime, waketime



    @classmethod
    def make_first_sleep_status(cls, valid_from, valid_to, goal_value, xp, user_id, frequency):
        goal_db = Goal.query.filter(Goal.user_id==user_id, Goal.xp==xp, Goal.goal_type=="Sleep", Goal.value==goal_value, Goal.valid_from==valid_from, Goal.valid_to==valid_to).first()
        print goal_db
        cls.save_sleep_goal_status(goal_db, "00:00", "00:00", frequency)

class Friendship(db.Model):

    __tablename__ = "friendships"

    friendship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    user_id_2 = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)


    def __repr__(self):
        return "<Friendship between user_id=%s and user_id=%s>"%(self.user_id_1, self.user_id_2)

class Team(db.Model):

    __tablename__ = "teams"

    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    teamname = db.Column(db.String(32), nullable=False)


    def __repr__(self):
        return "<Team teamname=%s>"% self.teamname

    def get_current_team_members(self):
        user_id_list = [userteam.user_id for userteam in self.userteam if userteam.valid_from < datetime.datetime.now() and userteam.valid_to > datetime.datetime.now()]
        return [User.query.get(user_id) for user_id in user_id_list]

class UserTeam(db.Model):

    __tablename__ = "userteams"

    userteam_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.team_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    valid_from = db.Column(db.TIMESTAMP, nullable=False)
    valid_to = db.Column(db.TIMESTAMP, nullable=True)

    user = db.relationship("User", backref=db.backref("userteam", order_by = valid_from))
    team = db.relationship("Team", backref=db.backref("userteam"))

    def __repr__(self):
        return "<UserTeam team_id=%s, user_id=%s>"%(self.team_id, self.user_id)



def connect_to_db(app, uri='postgresql:///natural20'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."