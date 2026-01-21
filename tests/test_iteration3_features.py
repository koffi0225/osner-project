"""
Test suite for Iteration 3 features:
1. About page (/a-propos) route
2. Contact page (/contact) route
3. Footer links to About and Contact
4. Notifications API endpoints
5. Welcome notification on user registration
"""

import pytest
import requests
import os
import uuid

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://osner-career.preview.emergentagent.com')


class TestAPIHealth:
    """Basic API health checks"""
    
    def test_api_root(self):
        """Test API root endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"✅ API root: {data['message']}")


class TestNotificationAPI:
    """Test notification system API endpoints"""
    
    @pytest.fixture(scope="class")
    def test_user(self):
        """Create a test user and return credentials"""
        unique_id = str(uuid.uuid4())[:8]
        email = f"test_notif_{unique_id}@test.com"
        password = "TestPassword123!"
        
        # Register user
        response = requests.post(f"{BASE_URL}/api/candidate/register", json={
            "email": email,
            "password": password,
            "nom": "Test",
            "prenom": "Notification",
            "sexe": "M",
            "telephone": "+225 00 00 00 00"
        })
        
        if response.status_code == 200:
            data = response.json()
            return {
                "email": email,
                "password": password,
                "token": data["access_token"],
                "user_id": data["user"]["id"]
            }
        else:
            pytest.skip(f"Could not create test user: {response.text}")
    
    def test_get_notifications_unauthenticated(self):
        """Test that notifications endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/notifications")
        assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"
        print("✅ Notifications endpoint requires authentication")
    
    def test_get_notifications_count_unauthenticated(self):
        """Test that notification count endpoint requires authentication"""
        response = requests.get(f"{BASE_URL}/api/notifications/count")
        assert response.status_code in [401, 403], f"Expected 401 or 403, got {response.status_code}"
        print("✅ Notification count endpoint requires authentication")
    
    def test_get_notifications_authenticated(self, test_user):
        """Test getting notifications for authenticated user"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = requests.get(f"{BASE_URL}/api/notifications", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Got {len(data)} notifications for user")
        
        # Check if welcome notification exists
        welcome_notifs = [n for n in data if n.get('type') == 'welcome']
        if welcome_notifs:
            print(f"✅ Welcome notification found: {welcome_notifs[0]['title']}")
        return data
    
    def test_get_unread_count_authenticated(self, test_user):
        """Test getting unread notification count"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = requests.get(f"{BASE_URL}/api/notifications/count", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "unread_count" in data
        assert isinstance(data["unread_count"], int)
        print(f"✅ Unread count: {data['unread_count']}")
    
    def test_welcome_notification_on_registration(self, test_user):
        """Verify that welcome notification was created on registration"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = requests.get(f"{BASE_URL}/api/notifications", headers=headers)
        
        assert response.status_code == 200
        notifications = response.json()
        
        # Find welcome notification
        welcome_notifs = [n for n in notifications if n.get('type') == 'welcome']
        assert len(welcome_notifs) > 0, "Welcome notification should be created on registration"
        
        welcome = welcome_notifs[0]
        assert "Bienvenue" in welcome['title']
        assert welcome['read'] == False
        assert welcome.get('link') == '/candidate/cv-upload'
        print(f"✅ Welcome notification verified: {welcome['title']}")
    
    def test_mark_notification_as_read(self, test_user):
        """Test marking a notification as read"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        
        # Get notifications first
        response = requests.get(f"{BASE_URL}/api/notifications", headers=headers)
        notifications = response.json()
        
        if not notifications:
            pytest.skip("No notifications to mark as read")
        
        notif_id = notifications[0]['id']
        
        # Mark as read
        response = requests.put(f"{BASE_URL}/api/notifications/{notif_id}/read", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        print(f"✅ Notification marked as read")
    
    def test_mark_all_as_read(self, test_user):
        """Test marking all notifications as read"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        
        response = requests.put(f"{BASE_URL}/api/notifications/read-all", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        print(f"✅ All notifications marked as read, count: {data.get('marked_count', 0)}")
    
    def test_delete_notification(self, test_user):
        """Test deleting a notification"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        
        # First create a new user to get fresh notifications
        unique_id = str(uuid.uuid4())[:8]
        email = f"test_delete_{unique_id}@test.com"
        
        reg_response = requests.post(f"{BASE_URL}/api/candidate/register", json={
            "email": email,
            "password": "TestPassword123!",
            "nom": "Delete",
            "prenom": "Test",
            "sexe": "F"
        })
        
        if reg_response.status_code != 200:
            pytest.skip("Could not create user for delete test")
        
        new_token = reg_response.json()["access_token"]
        new_headers = {"Authorization": f"Bearer {new_token}"}
        
        # Get notifications
        response = requests.get(f"{BASE_URL}/api/notifications", headers=new_headers)
        notifications = response.json()
        
        if not notifications:
            pytest.skip("No notifications to delete")
        
        notif_id = notifications[0]['id']
        
        # Delete notification
        response = requests.delete(f"{BASE_URL}/api/notifications/{notif_id}", headers=new_headers)
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        print(f"✅ Notification deleted successfully")


class TestCandidateAuth:
    """Test candidate authentication for notification context"""
    
    def test_register_new_user(self):
        """Test user registration creates welcome notification"""
        unique_id = str(uuid.uuid4())[:8]
        email = f"test_reg_{unique_id}@test.com"
        
        response = requests.post(f"{BASE_URL}/api/candidate/register", json={
            "email": email,
            "password": "TestPassword123!",
            "nom": "Registration",
            "prenom": "Test",
            "sexe": "M",
            "telephone": "+225 00 00 00 00"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == email
        print(f"✅ User registered: {email}")
        
        # Verify welcome notification was created
        headers = {"Authorization": f"Bearer {data['access_token']}"}
        notif_response = requests.get(f"{BASE_URL}/api/notifications", headers=headers)
        
        assert notif_response.status_code == 200
        notifications = notif_response.json()
        welcome_notifs = [n for n in notifications if n.get('type') == 'welcome']
        assert len(welcome_notifs) > 0, "Welcome notification should exist after registration"
        print(f"✅ Welcome notification created for new user")
    
    def test_login_existing_user(self):
        """Test login for existing user"""
        # First register
        unique_id = str(uuid.uuid4())[:8]
        email = f"test_login_{unique_id}@test.com"
        password = "TestPassword123!"
        
        reg_response = requests.post(f"{BASE_URL}/api/candidate/register", json={
            "email": email,
            "password": password,
            "nom": "Login",
            "prenom": "Test",
            "sexe": "F"
        })
        
        if reg_response.status_code != 200:
            pytest.skip("Could not register user for login test")
        
        # Now login
        response = requests.post(f"{BASE_URL}/api/candidate/login", json={
            "email": email,
            "password": password
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        print(f"✅ User logged in successfully")


class TestExistingEndpoints:
    """Verify existing endpoints still work"""
    
    def test_articles_endpoint(self):
        """Test articles endpoint"""
        response = requests.get(f"{BASE_URL}/api/articles?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Articles endpoint: {len(data)} articles")
    
    def test_formations_endpoint(self):
        """Test formations endpoint"""
        response = requests.get(f"{BASE_URL}/api/formations?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Formations endpoint: {len(data)} formations")
    
    def test_emplois_endpoint(self):
        """Test emplois endpoint"""
        response = requests.get(f"{BASE_URL}/api/emplois?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Emplois endpoint: {len(data)} emplois")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
