from unittest import TestCase
from server import app
from model import db, connect_to_db, User, UserStatus, LevelLookup, Goal, GoalStatus, Monster, Attack, SleepStatus
import server
import datetime
from selenium import webdriver
import time
from freezegun import freeze_time

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



class UserTest(TestCase):

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

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_userpage(self):

        result = self.client.get("/user/ToK")
        self.assertIn("Welcome, ToK!", result.data)
        self.assertIn("Log Out", result.data)
        self.assertIn("Your current quest is to complete 100 Steps", result.data)

    def test_outcome_json(self):
        result = self.client.get("/outcome.json")
        self.assertIn("monster", result.data)
        self.assertIn("attack", result.data)


    def test_settings_page(self):
        result = self.client.get("/settings")
        self.assertIn("Email address: test@test.com", result.data)
        self.assertIn("Log Out", result.data)

    def test_enter_sleep_page(self):
        result = self.client.get("/enter_sleep")
        self.assertIn("Bedtime", result.data)
        self.assertIn("Wake up time", result.data)

    def test_set_goal_page(self):
        result = self.client.get("/set_goal")
        self.assertIn("Goal value", result.data)
        self.assertIn("Quest type:", result.data)


    def test_set_goal(self):
        server.flow.step1_get_authorize_url=_mock_auth
        result = self.client.post("/set_goal", data={"goal_type":"Steps",
                                                      "valid_from": "2017-10-03",
                                                      "valid_to": "2017-10-10",
                                                      "value": 100000,
                                                      "frequency": "Total"}, follow_redirects=True)
        self.assertIn("Your current quest is to complete 100000 Steps",result.data)

    def test_set_goal_sleep(self):
        server.flow.step1_get_authorize_url=_mock_auth
        result = self.client.post("/set_goal", data={"goal_type":"Steps",
                                                      "valid_from": "2017-10-03",
                                                      "valid_to": "2017-10-10",
                                                      "value": 8*60*60,
                                                      "frequency": "Daily"}, follow_redirects=True)
        self.assertIn("Your current quest is to complete 8.0 hours of Sleep",result.data)


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

    def test_calc_xp(self):
        result = self.client.get("/calc_xp.json", query_string={"goal_type": "Steps", "value": 2000000,
                                                        "frequency": "Total", "valid_from":"2017-10-02",
                                                        "valid_to":"2017-10-03"}, follow_redirects=True)
        self.assertIn("500", result.data)

    def test_update_settings_json(self):
        result = self.client.post("/update_settings.json", data={"email":"test2@test.com", "confirm_email": "test2@test.com"},
                                follow_redirects=True)
        self.assertIn("test2@test.com", result.data)
        result = self.client.get("/settings")
        self.assertIn("Email address: test2@test.com", result.data)

    def test_logout(self):
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("You are now logged out", result.data)
        self.assertIn("Log In", result.data)


class SeleniumTests(TestCase):

    def setUp(self):
        self.browser_type = "Firefox"
        if self.browser_type == "Firefox":
            self.browser = webdriver.Firefox()
        elif self.browser_type == "Chrome":
            self.browser = webdriver.Chrome()
        server.flow.step1_get_authorize_url=_mock_auth
        self.browser.get("http://localhost:5000/login")
        username = self.browser.find_element_by_id('username')
        username.send_keys("ToK")
        password = self.browser.find_element_by_id('password')
        password.send_keys("1234")
        submit = self.browser.find_element_by_id("submit")
        submit.click()

    def tearDown(self):
        self.browser.quit()
       

    def test_set_goal(self):
        self.browser.get('http://localhost:5000/set_goal')

        x = self.browser.find_element_by_id('valid_from')
        
        y = self.browser.find_element_by_id('valid_to')
        if self.browser_type == "Firefox":
            x.send_keys("2017-10-01")
            y.send_keys("2017-10-02")
        elif self.browser_type == "Chrome":
            x.send_keys("10-01-2017")
            y.send_keys("10-02-2017")

        y = self.browser.find_element_by_id('value')
        y.send_keys("20000")

        btn = self.browser.find_element_by_id('calc_xp')
        btn.click()

        result = self.browser.find_element_by_id('show_xp')
        self.assertEqual(result.text, "500")





def example_data():
    user = User(username="ToK", password="1234", email="test@test.com")
    l = LevelLookup(level=1, min_cr =0, max_cr=0.25, required_xp=0, hit_point_max=12)
    db.session.add_all([user,l])
    db.session.commit()
    user = User.query.filter(User.username=="ToK").one()
    us = UserStatus(user_id=user.user_id, current_xp=20, current_hp=12, level=1, date_recorded=datetime.datetime.now())
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

    print User.query.all()


if __name__ == "__main__":
    import unittest

    unittest.main()