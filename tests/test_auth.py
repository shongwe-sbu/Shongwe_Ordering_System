import unittest

from app.auth import ADMIN_ROLE, EMPLOYEE_ROLE, authenticate, clear_users, register_user


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        clear_users()
        register_user("admin1", "admin123", ADMIN_ROLE)
        register_user("emp1", "emp123", EMPLOYEE_ROLE)

    def test_admin_login_authenticates_successfully(self):
        user = authenticate("admin1", "admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "admin1")
        self.assertEqual(user["role"], ADMIN_ROLE)

    def test_employee_login_authenticates_successfully(self):
        user = authenticate("emp1", "emp123")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "emp1")
        self.assertEqual(user["role"], EMPLOYEE_ROLE)

    def test_wrong_password_fails(self):
        user = authenticate("emp1", "wrongpass")
        self.assertIsNone(user)

    def test_role_mismatch_is_rejected(self):
        user = authenticate("emp1", "emp123", ADMIN_ROLE)
        self.assertIsNone(user)

    def test_duplicate_username_is_rejected(self):
        with self.assertRaises(ValueError):
            register_user("emp1", "anotherpass", EMPLOYEE_ROLE)


if __name__ == "__main__":
    unittest.main()
