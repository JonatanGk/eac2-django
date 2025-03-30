from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By

class PasswordValidationTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True


        # creem usuari tipus staff
        cls.staff_user = User.objects.create_user("staffuser", "staff@example.com", "temporarypass123")
        cls.staff_user.is_staff = True
        cls.staff_user.save()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_validate_password_rules(self):
        self.selenium.get(f'{self.live_server_url}/admin/')

        # fem login
        self.selenium.find_element(By.NAME, "username").send_keys("staffuser")
        self.selenium.find_element(By.NAME, "password").send_keys("temporarypass123")
        self.selenium.find_element(By.XPATH, "//input[@value='Log in']").click()

        # click butó "CHANGE PASSWORD"
        self.selenium.find_element(By.LINK_TEXT, "CHANGE PASSWORD").click()

        # fem get del contenidor del formulari del help
        password_help = self.selenium.find_element(By.ID, "id_new_password1_helptext").text

        assert "Your password can’t be too similar to your other personal information." in password_help
        assert "Your password must contain at least 8 characters." in password_help
        assert "Your password can’t be a commonly used password." in password_help
        assert "Your password can’t be entirely numeric." in password_help
