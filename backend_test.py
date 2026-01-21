import requests
import sys
import json
from datetime import datetime

class PlatformAPITester:
    def __init__(self, base_url="https://osner-career.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details
        })

    def test_api_root(self):
        """Test API root endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Message: {data.get('message', 'No message')}"
            self.log_test("API Root", success, details)
            return success
        except Exception as e:
            self.log_test("API Root", False, str(e))
            return False

    def test_get_articles(self):
        """Test getting articles"""
        try:
            response = requests.get(f"{self.api_url}/articles", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                articles = response.json()
                details += f", Count: {len(articles)}"
                # Check if we have the expected seeded articles
                if len(articles) >= 4:
                    details += " (Expected seeded data found)"
                else:
                    details += " (Warning: Less than expected 4 articles)"
            self.log_test("Get Articles", success, details)
            return success, response.json() if success else []
        except Exception as e:
            self.log_test("Get Articles", False, str(e))
            return False, []

    def test_get_featured_articles(self):
        """Test getting featured articles"""
        try:
            response = requests.get(f"{self.api_url}/articles?vedette=true", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                articles = response.json()
                details += f", Featured count: {len(articles)}"
                # Check if we have featured articles
                if len(articles) >= 3:
                    details += " (Expected 3 featured articles found)"
            self.log_test("Get Featured Articles", success, details)
            return success
        except Exception as e:
            self.log_test("Get Featured Articles", False, str(e))
            return False

    def test_get_article_by_slug(self, articles):
        """Test getting article by slug"""
        if not articles:
            self.log_test("Get Article by Slug", False, "No articles available for testing")
            return False
        
        try:
            test_article = articles[0]
            slug = test_article.get('slug')
            if not slug:
                self.log_test("Get Article by Slug", False, "No slug found in article")
                return False
                
            response = requests.get(f"{self.api_url}/articles/{slug}", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Slug: {slug}"
            if success:
                article = response.json()
                details += f", Title: {article.get('titre', 'No title')}"
            self.log_test("Get Article by Slug", success, details)
            return success
        except Exception as e:
            self.log_test("Get Article by Slug", False, str(e))
            return False

    def test_get_formations(self):
        """Test getting formations"""
        try:
            response = requests.get(f"{self.api_url}/formations", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                formations = response.json()
                details += f", Count: {len(formations)}"
                if len(formations) >= 3:
                    details += " (Expected seeded data found)"
            self.log_test("Get Formations", success, details)
            return success, response.json() if success else []
        except Exception as e:
            self.log_test("Get Formations", False, str(e))
            return False, []

    def test_get_formation_by_slug(self, formations):
        """Test getting formation by slug"""
        if not formations:
            self.log_test("Get Formation by Slug", False, "No formations available for testing")
            return False
        
        try:
            test_formation = formations[0]
            slug = test_formation.get('slug')
            if not slug:
                self.log_test("Get Formation by Slug", False, "No slug found in formation")
                return False
                
            response = requests.get(f"{self.api_url}/formations/{slug}", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Slug: {slug}"
            if success:
                formation = response.json()
                details += f", Title: {formation.get('titre', 'No title')}"
            self.log_test("Get Formation by Slug", success, details)
            return success
        except Exception as e:
            self.log_test("Get Formation by Slug", False, str(e))
            return False

    def test_get_emplois(self):
        """Test getting job offers"""
        try:
            response = requests.get(f"{self.api_url}/emplois", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                emplois = response.json()
                details += f", Count: {len(emplois)}"
                if len(emplois) >= 4:
                    details += " (Expected seeded data found)"
            self.log_test("Get Job Offers", success, details)
            return success, response.json() if success else []
        except Exception as e:
            self.log_test("Get Job Offers", False, str(e))
            return False, []

    def test_get_emploi_by_slug(self, emplois):
        """Test getting job offer by slug"""
        if not emplois:
            self.log_test("Get Job Offer by Slug", False, "No job offers available for testing")
            return False
        
        try:
            test_emploi = emplois[0]
            slug = test_emploi.get('slug')
            if not slug:
                self.log_test("Get Job Offer by Slug", False, "No slug found in job offer")
                return False
                
            response = requests.get(f"{self.api_url}/emplois/{slug}", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Slug: {slug}"
            if success:
                emploi = response.json()
                details += f", Title: {emploi.get('titre', 'No title')}"
            self.log_test("Get Job Offer by Slug", success, details)
            return success
        except Exception as e:
            self.log_test("Get Job Offer by Slug", False, str(e))
            return False

    def test_newsletter_subscription(self):
        """Test newsletter subscription"""
        try:
            test_email = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
            response = requests.post(
                f"{self.api_url}/newsletter",
                json={"email": test_email},
                timeout=10
            )
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Email: {test_email}"
            if success:
                data = response.json()
                details += f", ID: {data.get('id', 'No ID')}"
            self.log_test("Newsletter Subscription", success, details)
            return success
        except Exception as e:
            self.log_test("Newsletter Subscription", False, str(e))
            return False

    def test_newsletter_duplicate_email(self):
        """Test newsletter subscription with duplicate email"""
        try:
            # Use a common email that might already exist
            test_email = "duplicate@example.com"
            
            # First subscription
            response1 = requests.post(
                f"{self.api_url}/newsletter",
                json={"email": test_email},
                timeout=10
            )
            
            # Second subscription (should fail)
            response2 = requests.post(
                f"{self.api_url}/newsletter",
                json={"email": test_email},
                timeout=10
            )
            
            success = response2.status_code == 400
            details = f"First: {response1.status_code}, Second: {response2.status_code}"
            if success:
                details += " (Correctly rejected duplicate)"
            else:
                details += " (Should have rejected duplicate)"
            
            self.log_test("Newsletter Duplicate Email", success, details)
            return success
        except Exception as e:
            self.log_test("Newsletter Duplicate Email", False, str(e))
            return False

    def test_article_filtering(self):
        """Test article filtering by category"""
        try:
            response = requests.get(f"{self.api_url}/articles?categorie=Société", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                articles = response.json()
                details += f", Filtered count: {len(articles)}"
                # Check if all articles have the correct category
                if articles:
                    correct_category = all(article.get('categorie') == 'Société' for article in articles)
                    details += f", Correct filtering: {correct_category}"
            self.log_test("Article Category Filtering", success, details)
            return success
        except Exception as e:
            self.log_test("Article Category Filtering", False, str(e))
            return False

    def test_formation_filtering(self):
        """Test formation filtering by level"""
        try:
            response = requests.get(f"{self.api_url}/formations?niveau=Débutant", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                formations = response.json()
                details += f", Filtered count: {len(formations)}"
            self.log_test("Formation Level Filtering", success, details)
            return success
        except Exception as e:
            self.log_test("Formation Level Filtering", False, str(e))
            return False

    def test_emploi_filtering(self):
        """Test job offer filtering by type"""
        try:
            response = requests.get(f"{self.api_url}/emplois?type=Emploi", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                emplois = response.json()
                details += f", Filtered count: {len(emplois)}"
            self.log_test("Job Offer Type Filtering", success, details)
            return success
        except Exception as e:
            self.log_test("Job Offer Type Filtering", False, str(e))
            return False

    def run_all_tests(self):
        """Run all backend API tests"""
        print("🚀 Starting Platform API Tests")
        print(f"Testing against: {self.base_url}")
        print("=" * 50)

        # Test API connectivity
        if not self.test_api_root():
            print("❌ API is not accessible. Stopping tests.")
            return False

        # Test articles endpoints
        articles_success, articles = self.test_get_articles()
        if articles_success:
            self.test_get_featured_articles()
            self.test_get_article_by_slug(articles)
            self.test_article_filtering()

        # Test formations endpoints
        formations_success, formations = self.test_get_formations()
        if formations_success:
            self.test_get_formation_by_slug(formations)
            self.test_formation_filtering()

        # Test emplois endpoints
        emplois_success, emplois = self.test_get_emplois()
        if emplois_success:
            self.test_get_emploi_by_slug(emplois)
            self.test_emploi_filtering()

        # Test newsletter
        self.test_newsletter_subscription()
        self.test_newsletter_duplicate_email()

        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.tests_passed}/{self.tests_run} passed")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_passed < self.tests_run:
            print("\n❌ Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")

        return self.tests_passed == self.tests_run

def main():
    tester = PlatformAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())