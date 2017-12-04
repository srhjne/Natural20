from unittest import TestCase
from server import app
from model import db, connect_to_db, User, UserStatus, LevelLookup, Goal, GoalStatus, Monster, Attack, SleepStatus, Friendship, Team, TeamInvite, UserTeam
import server
import datetime
from selenium import webdriver
import time
from freezegun import freeze_time
import bcrypt


def _mock_auth():
            return "/"

class NoUserTest(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()


    def test_login_page(self):
        result = self.client.get("/login")
        self.assertIn("Username", result.data)
        self.assertIn("Password", result.data)
        self.assertIn("Login", result.data)
        self.assertNotIn("Logout", result.data)


    def test_login(self):
        
        server.flow.step1_get_authorize_url=_mock_auth

        result = self.client.post("/login",
                              data={"username": "ToK",
                                    "password": "1234"},
                              follow_redirects=True)
        self.assertIn("Welcome, ToK", result.data)
        self.assertNotIn("Login", result.data)

    def test_homepage(self):
        result = self.client.get("/", follow_redirects=True)
        self.assertIn("Login", result.data)

    def test_registration_page(self):
        result = self.client.get("/registration", follow_redirects=True)
        self.assertIn("Log In", result.data)
        self.assertIn("Confirm password", result.data)
        self.assertIn("Username", result.data)
        self.assertNotIn("Login", result.data)

    def test_registration(self):
        result = self.client.post("/registration", data={"username":"Bob",
                                                         "password": "1111",
                                                          "email": "bob@bob.com",
                                                          "confirm_password": "1111"}, follow_redirects=True)
        self.assertIn("Thanks for registering!", result.data)
        result = self.client.get("/user/Bob",follow_redirects=True)
        self.assertNotIn("This page does not exist", result.data)

    def test_registration_fail(self):
        result = self.client.post("/registration", data={"username":"ToK",
                                                         "password": "1111",
                                                          "email": "bob@bob.com",
                                                          "confirm_password": "1111"}, follow_redirects=True)
        self.assertNotIn("Thanks for registering!", result.data)
        self.assertIn("Sorry that username is already taken!", result.data)

    @freeze_time("2017-01-01")
    def test_clock_json(self):
        result = self.client.get("/clock.json")
        self.assertIn("01 January 2017", result.data)



class UserTest3rdOct(TestCase):

    @freeze_time("2017-10-03")
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        app.config['SECRET_KEY'] = 'key'
        with self.client as c:
          with c.session_transaction() as sess:
              sess['user_id'] = 1
              sess["login_time"] = datetime.datetime.now()

    @freeze_time("2017-10-03")
    def tearDown(self):
        db.session.close()
        db.drop_all()

    @freeze_time("2017-10-03")
    def test_userpage(self):

        result = self.client.get("/user/ToK")
        self.assertIn("Welcome, ToK!", result.data)
        self.assertIn("Log Out", result.data)
        self.assertIn("current quest is to complete 100 Steps", result.data)

    @freeze_time("2017-10-03")
    def test_userpage_friend(self):

        result = self.client.get("/user/Test2_friend", follow_redirects=True)
        self.assertNotIn("Welcome", result.data)
        self.assertIn("Test2_friend's profile", result.data)
        self.assertIn("Log Out", result.data)

    @freeze_time("2017-10-03")
    def test_userpage_notfriend(self):

        result = self.client.get("/user/Test_friend", follow_redirects=True)
        self.assertIn("Welcome", result.data)
        self.assertIn("You must be friends with Test_friend to view their page", result.data)
        self.assertIn("Log Out", result.data)


    @freeze_time("2017-10-04")
    def test_userpage_timeout(self):

        result = self.client.get("/user/ToK", follow_redirects=True)
        self.assertNotIn("Welcome, ToK!", result.data)
        self.assertIn("please log in again", result.data)


    @freeze_time("2017-10-03")
    def test_outcome_json(self):
        result = self.client.get("/outcome.json")
        self.assertIn("monster", result.data)
        self.assertIn("attack", result.data)
        result = self.client.get("/user/Test2_friend")
        self.assertIn("11", result.data)
        self.assertNotIn("HP: 12", result.data)

    @freeze_time("2017-10-03")
    def test_settings_page(self):
        result = self.client.get("/settings")
        self.assertIn("Email address: test@test.com", result.data)
        self.assertIn("Log Out", result.data)

    @freeze_time("2017-10-03")
    def test_enter_sleep_page(self):
        result = self.client.get("/enter_sleep")
        self.assertIn("Bedtime", result.data)
        self.assertIn("Wake up time", result.data)

    @freeze_time("2017-10-03")
    def test_set_goal_page(self):
        result = self.client.get("/set_goal")
        self.assertIn("Goal value", result.data)
        self.assertIn("Quest type:", result.data)

    @freeze_time("2017-10-04")
    def test_set_goal(self):
        with self.client as c:
          with c.session_transaction() as sess:
              sess['user_id'] = 1
              sess["login_time"] = datetime.datetime.now()
        server.flow.step1_get_authorize_url=_mock_auth
        result = self.client.post("/set_goal", data={"goal_type":"Steps",
                                                      "valid_from": "2017-10-03",
                                                      "valid_to": "2017-10-10",
                                                      "value": 100000,
                                                      "frequency": "Total"}, follow_redirects=True)
        self.assertIn("current quest is to complete 100000 Steps",result.data)

    @freeze_time("2017-10-03")
    def test_set_goal_sleep(self):
        server.flow.step1_get_authorize_url=_mock_auth
        result = self.client.post("/set_goal", data={"goal_type":"Steps",
                                                      "valid_from": "2017-10-03",
                                                      "valid_to": "2017-10-10",
                                                      "value": 8*60*60,
                                                      "frequency": "Daily"}, follow_redirects=True)
        self.assertIn("current quest is to complete 8.0 hours of Sleep",result.data)


    @freeze_time("2017-10-03")
    def test_reroll(self):
        result = self.client.post("/reroll", data={}, follow_redirects=True)
        self.assertIn("XP: 0", result.data)
        self.assertNotIn("XP: 20", result.data)

    @freeze_time("2017-10-02")
    def test_enter_sleep(self):
        result = self.client.post("/enter_sleep",data={"bedtime":"22:00","waketime":"06:00"},
                                 follow_redirects=True)
        self.assertIn("Welcome, ToK!", result.data)

        result = self.client.get("/goal_graph.json")
        self.assertIn(str(8*60*60),result.data)
        self.assertIn("bedtime", result.data)

    @freeze_time("2017-10-02")
    def test_calc_xp(self):
        result = self.client.get("/calc_xp.json", query_string={"goal_type": "Steps", "value": 2000000,
                                                        "frequency": "Total", "valid_from":"2017-10-02",
                                                        "valid_to":"2017-10-03"}, follow_redirects=True)
        self.assertIn("500", result.data)

    @freeze_time("2017-10-03")
    def test_update_settings_json(self):
        result = self.client.post("/update_settings.json", data={"email":"test2@test.com", "confirm_email": "test2@test.com"},
                                follow_redirects=True)
        self.assertIn("test2@test.com", result.data)
        result = self.client.get("/settings")
        self.assertIn("Email address: test2@test.com", result.data)

    @freeze_time("2017-10-03")
    def test_logout(self):
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("You are now logged out", result.data)
        self.assertIn("Log In", result.data)

    @freeze_time("2017-10-03")
    def test_users_json(self):
        result = self.client.get("/users.json", query_string={"search_term":""})
        self.assertIn("Test_friend", result.data)

    @freeze_time("2017-10-03")
    def test_friend_requests_json(self):
        result = self.client.get("/friend_request.json")
        self.assertIn("Test_friend", result.data)

    @freeze_time("2017-10-03")
    def test_friend_request_post(self):
        result = self.client.post("/friend_request.json", data={"friendship_id":1})
        self.assertIn("1",result.data)
        result = self.client.get("/friend_request.json")
        self.assertEqual("[]\n", result.data)
        result = self.client.get("/friends")
        self.assertIn("Test_friend", result.data)

    @freeze_time("2017-10-03")
    def test_add_friend_json(self):
        result = self.client.post("/add_friend.json",data={"user_id":2})
        self.assertIn("success", result.data)
     
    
    @freeze_time("2017-10-03")
    def test_make_new_team_json(self):
        result = self.client.post("/make_new_team.json", data={"teamname":"What_a_lovely_team"})
        self.assertIn("What_a_lovely_team", result.data)

    @freeze_time("2017-10-03")
    def test_get_friends_json(self):
        result = self.client.get("/get_friends.json")
        self.assertIn("Test2_friend", result.data)
        self.assertNotIn("Test_friend", result.data)

    @freeze_time("2017-10-03")
    def test_goal_graph_json_friend(self):
        result = self.client.get("/goal_graph.json", query_string={"username":"Test2_friend"})
        self.assertNotIn("series", result.data)

    @freeze_time("2017-10-03")
    def test_goal_graph_json_friend(self):
        result = self.client.get("/goal_graph.json", query_string={"username":None})
        self.assertIn("series", result.data)
        self.assertIn("100", result.data)
        self.assertNotIn("10000", result.data)




class UserTest4thOct(TestCase):

    @freeze_time("2017-10-03")
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

        app.config['SECRET_KEY'] = 'key'
        with self.client as c:
          with c.session_transaction() as sess:
              sess['user_id'] = 1
              sess["login_time"] = datetime.datetime.strptime('2017-10-04','%Y-%m-%d')

    @freeze_time("2017-10-04")
    def tearDown(self):
        db.session.close()
        db.drop_all()


    @freeze_time("2017-10-04")
    def test_leave_team_json(self):
        result = self.client.post("/leave_team.json", data={"teamname": "test_team"})
        self.assertIn("test_team", result.data)
        result = self.client.get("/get_team.json",query_string={"teamname":"test_team"})
        self.assertNotIn("ToK", result.data)

    @freeze_time("2017-10-04")
    def test_get_team_requests_json(self):
        result = self.client.get("/get_team_requests.json")
        self.assertIn("Test_friend", result.data)
        self.assertIn("test_team2", result.data)

    @freeze_time("2017-10-04")
    def test_join_team_json(self):
        result = self.client.post("/join_team.json", data={"invite_id":1, "teamname":"test_team2"})
        self.assertIn("test_team2", result.data)
        result = self.client.get("/get_team.json",query_string={"teamname":"test_team"})
        self.assertNotIn("ToK", result.data)
        result = self.client.get("/get_team_requests.json")
        self.assertNotIn("Test_friend", result.data)
        self.assertNotIn("test_team2", result.data)


    @freeze_time("2017-10-04")
    def test_get_team_json(self):
        result = self.client.get("/get_team.json",query_string={"teamname":"test_team"})
        self.assertIn("ToK", result.data)
        result = self.client.get("/get_team.json",query_string={"teamname":""})
        self.assertIn("ToK", result.data)

    @freeze_time("2017-10-04")   
    def test_get_leaderboard_json(self):
        result = self.client.get("/get_leaderboard.json")
        self.assertIn("test_team", result.data)
        self.assertIn("20", result.data)

    @freeze_time("2017-10-04")
    def test_invite_friend_json(self):
        result = self.client.post("/invite_friend.json", data={"friendname":"Test_friend"})
        self.assertIn("Test_friend was invited to join test_team", result.data)


# class SeleniumTests(TestCase):

#     def setUp(self):
#         self.browser_type = "Firefox"
#         if self.browser_type == "Firefox":
#             self.browser = webdriver.Firefox()
#         elif self.browser_type == "Chrome":
#             self.browser = webdriver.Chrome()
#         server.flow.step1_get_authorize_url=_mock_auth
#         self.browser.get("http://localhost:5000/login")
#         username = self.browser.find_element_by_id('username')
#         username.send_keys("ToK")
#         password = self.browser.find_element_by_id('password')
#         password.send_keys("1234")
#         submit = self.browser.find_element_by_id("submit")
#         submit.click()

#     def tearDown(self):
#         self.browser.quit()
       

#     def test_set_goal(self):
#         self.browser.get('http://localhost:5000/set_goal')

#         x = self.browser.find_element_by_id('valid_from')
        
#         y = self.browser.find_element_by_id('valid_to')
#         if self.browser_type == "Firefox":
#             x.send_keys("2017-10-01")
#             y.send_keys("2017-10-02")
#         elif self.browser_type == "Chrome":
#             x.send_keys("10-01-2017")
#             y.send_keys("10-02-2017")

#         y = self.browser.find_element_by_id('value')
#         y.send_keys("20000")

#         btn = self.browser.find_element_by_id('calc_xp')
#         btn.click()

#         result = self.browser.find_element_by_id('show_xp')
#         self.assertEqual(result.text, "500")





def example_data():
    hashed_password = bcrypt.hashpw("1234", bcrypt.gensalt(10))
    user = User(username="ToK", password=hashed_password, email="test@test.com", timezone="Etc/UTC")
    if not LevelLookup.query.get(1):
        l = LevelLookup(level=1, min_cr =0, max_cr=0.25, required_xp=0, hit_point_max=12)
        db.session.add(l)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter(User.username=="ToK").one()
    us = UserStatus(user_id=user.user_id, current_xp=20, current_hp=12, level=1, date_recorded=datetime.datetime.strptime("01-10-2017", "%d-%m-%Y"))
    valid_from = datetime.datetime.strptime("01-10-2017", "%d-%m-%Y")
    print valid_from, type(valid_from)
    valid_to = datetime.datetime.strptime("07-10-2017", "%d-%m-%Y")
    valid_to2 = datetime.datetime.strptime("02-10-2017", "%d-%m-%Y")
    goal = Goal(user_id=user.user_id, xp=300, goal_type="Steps", frequency="Daily", value=100, valid_from=valid_from, valid_to=valid_to)
    goal2 = Goal(user_id=user.user_id, xp=300, goal_type="Steps", value=10000, valid_from=valid_from, valid_to=valid_to2)
    goal3 = Goal(user_id=user.user_id, xp=300, goal_type="Sleep", frequency="Daily", value=8*60*60, valid_from=valid_from, valid_to=valid_to)
    db.session.add_all([us, goal, goal2, goal3])
    db.session.commit()
    goal = Goal.query.filter(Goal.frequency=="Daily").first()
    gs = GoalStatus(value=0, date_recorded=valid_from, goal_id=goal.goal_id)
    goal = Goal.query.filter(Goal.frequency.is_(None)).first()
    gs2 = GoalStatus(value=0, date_recorded=valid_from, goal_id=goal.goal_id)
    db.session.add_all([gs,gs2])
    db.session.commit()
    SleepStatus.make_first_sleep_status(valid_from, valid_to, 8*60*60, 300, user.user_id, "Daily")
    monster = Monster(monster_id = 1, cr=0.1, name="Test Monster")
    db.session.add(monster)
    attack = Attack(monster_id=1, name="test attack", damage_type="piercing",
                        avg_damage=10, num_dice=1, type_dice=8,
                        dice_modifier=6)
    db.session.add(attack)
    db.session.commit()


    user2 = User(username="Test_friend", password=hashed_password, email="test2@test.com", timezone="Etc/UTC")
    db.session.add(user2)
    db.session.commit()
    user2 = User.query.filter(User.username=="Test_friend").one()
    us = UserStatus(user_id=user2.user_id, current_xp=20, current_hp=12, level=1, date_recorded=datetime.datetime.now())
    db.session.add(us)
    db.session.commit()

    user3 = User(username="Test2_friend", password=hashed_password, email="test2@test.com", timezone="Etc/UTC")
    db.session.add(user3)
    db.session.commit()
    user3 = User.query.filter(User.username=="Test2_friend").one()
    us2 = UserStatus(user_id=user3.user_id, current_xp=20, current_hp=12, level=1, date_recorded=datetime.datetime.now())
    db.session.add(us2)
    db.session.commit()

    fs = Friendship(user_id_1=user2.user_id, user_id_2=user.user_id, verified=False)
    db.session.add(fs)
    db.session.commit()

    fs2 = Friendship(user_id_1=user3.user_id, user_id_2=user.user_id, verified=True)
    db.session.add(fs2)
    db.session.commit()

    team = Team.create_team("test_team", 1)
    userteam = UserTeam(user_id=user3.user_id, team_id=1,valid_from=valid_from, valid_to=valid_to)
    db.session.add(userteam)
    db.session.commit()
    team2 = Team.create_team("test_team2", 2)

    print "TEAM STUFF USER 1", user.userteam[0].valid_from, user.userteam[0].valid_to
    print "TEAM STUFF USER 2", user2.userteam[0].valid_from, user2.userteam[0].valid_to

    teaminvite = TeamInvite(user_id=user.user_id, inviter_id=2, team_id=2, resolved=False)
    db.session.add(teaminvite)
    db.session.commit()

    print User.query.all()


if __name__ == "__main__":
    import unittest

    unittest.main()