from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError

class UsersTests(TestCase):
    """Test for user model"""
    
    def setUp(self):
        """initial config for all test"""
        self.email = 'normal@user.com'
        self.payload = {"email":self.email, "password":'12345F678@'}
        

    def test_constraints_of_password_of_user(self):
        """test for not create an user whitout constraints of password"""
        
        User = get_user_model()
        
        # failded because it does not meet the minimun lenght 
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(self.email, "F1@")
        
        # failded because it does not have capitalize letter
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(self.email, "12345678@")
        
        # failded because it does not have special character
        with self.assertRaises(ValidationError):
            user = User.objects.create_user(self.email, "12F345678")
 
    def test_constraints_of_password_of_superuser(self):
        """test for not create a superuser whitout constraints of password"""
        
        User = get_user_model()
        
        # failded because it does not meet the minimun lenght 
        with self.assertRaises(ValidationError):
            user = User.objects.create_superuser(self.email, "F1@")
        
        # failded because it does not have capitalize letter
        with self.assertRaises(ValidationError):
            user = User.objects.create_superuser(self.email, "12345678@")
        
        # failded because it does not have special character
        with self.assertRaises(ValidationError):
            user = User.objects.create_superuser(self.email, "12F345678")           
            

    def test_create_user_sussecsfull(self):
        """test for create user whit email"""
        
        User = get_user_model()
        user = User.objects.create_user(**self.payload)
        
        self.assertEqual(user.email, self.payload["email"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        self.assertTrue(user.check_password(self.payload["password"]), self.payload["password"])
        
    def test_create_superuser_sussecsfull(self):
        """test for create superuser whit email"""
        
        User = get_user_model()
        user = User.objects.create_superuser(**self.payload)
        
        self.assertEqual(user.email, self.payload["email"])
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        
        self.assertTrue(user.check_password(self.payload["password"]), self.payload["password"])
