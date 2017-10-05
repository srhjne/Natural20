from unittest import TestCase
from server import app
from model import db, connect_to_db, User, UserStatus, LevelLookup, Goal, GoalStatus
import server
import datetime
from selenium import webdriver
import time

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

        # del sess['user_id']

    def test_userpage(self):

        result = self.client.get("/user/ToK")
        self.assertIn("Welcome, ToK!", result.data)
        self.assertIn("Log Out", result.data)
        self.assertIn("Your current quest is to complete 100 Steps", result.data)


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


class SeleniumTests(TestCase):

    def setUp(self):
        self.browser_type = "Firefox"
        if self.browser_type == "Firefox":
            self.browser = webdriver.Firefox()
        elif self.browser_type == "Chrome":
            self.browser = webdriver.Chrome()
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()
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
        db.session.close()
        db.drop_all()

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

        time.sleep(10)
        result = self.browser.find_element_by_id('show_xp')
        self.assertEqual(result.text, "500")





def example_data():
    user = User(username="ToK", password="1234", email="test@test.com")
    l = LevelLookup(level=1, min_cr =0, max_cr=0.25, required_xp=0, hit_point_max=12)
    db.session.add_all([user,l])
    db.session.commit()
    user = User.query.filter(User.username=="ToK").one()
    us = UserStatus(user_id=user.user_id, current_xp=0, current_hp=12, level=1, date_recorded=datetime.datetime.now())
    valid_from = datetime.datetime.strptime("01-10-2017", "%d-%m-%Y")
    print valid_from, type(valid_from)
    valid_to = datetime.datetime.strptime("07-10-2017", "%d-%m-%Y")
    goal = Goal(user_id=user.user_id, xp=300, goal_type="Steps", frequency="Daily", value=100, valid_from=valid_from, valid_to=valid_to)
    db.session.add_all([us, goal])
    db.session.commit()
    goal = Goal.query.first()
    gs = GoalStatus(value=0, date_recorded=valid_from, goal_id=goal.goal_id)
    db.session.add(gs)
    db.session.commit()
    print User.query.all()


if __name__ == "__main__":
    import unittest

    unittest.main()