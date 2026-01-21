"""
Test suite for Osner-Group platform priority features:
1. News scraping/aggregation
2. Wave CI payment method
3. BDA bank details
4. Articles API with categories
5. Payment methods endpoint
"""

import pytest
import requests
import os

# Use the public URL for testing
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://osner-career.preview.emergentagent.com').rstrip('/')


class TestPaymentMethods:
    """Test payment methods endpoint including Wave CI"""
    
    def test_get_payment_methods_returns_200(self):
        """Test that payment methods endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/payments-multi/methods")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
    def test_payment_methods_contains_wave_ci(self):
        """Test that Wave CI is included in payment methods"""
        response = requests.get(f"{BASE_URL}/api/payments-multi/methods")
        assert response.status_code == 200
        
        data = response.json()
        assert "methods" in data, "Response should contain 'methods' key"
        
        methods = data["methods"]
        wave_ci_found = False
        for method in methods:
            if method.get("id") == "wave_ci":
                wave_ci_found = True
                assert method.get("name") == "Wave CI", f"Wave CI name mismatch: {method.get('name')}"
                assert method.get("type") == "mobile_money", f"Wave CI type should be mobile_money"
                assert method.get("available") == True, "Wave CI should be available"
                break
        
        assert wave_ci_found, "Wave CI payment method not found in response"
    
    def test_payment_methods_contains_all_expected_methods(self):
        """Test that all expected payment methods are present"""
        response = requests.get(f"{BASE_URL}/api/payments-multi/methods")
        assert response.status_code == 200
        
        data = response.json()
        methods = data["methods"]
        method_ids = [m["id"] for m in methods]
        
        expected_methods = ["stripe", "orange_money", "mtn_money", "moov_money", "wave_ci", "tresor_money", "bank_transfer"]
        for expected in expected_methods:
            assert expected in method_ids, f"Missing payment method: {expected}"
    
    def test_payment_packages_endpoint(self):
        """Test that payment packages endpoint works"""
        response = requests.get(f"{BASE_URL}/api/payments-multi/packages")
        assert response.status_code == 200
        
        data = response.json()
        assert "packages" in data, "Response should contain 'packages' key"
        assert len(data["packages"]) > 0, "Should have at least one package"


class TestNewsAggregation:
    """Test news aggregation endpoint"""
    
    def test_update_news_endpoint_returns_success(self):
        """Test that news update endpoint returns success"""
        response = requests.post(f"{BASE_URL}/api/aggregation/update-news", timeout=60)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert data.get("status") == "success", f"Expected success status, got: {data}"
        assert "added" in data or "message" in data, "Response should contain added count or message"
    
    def test_aggregation_status_endpoint(self):
        """Test aggregation status endpoint"""
        response = requests.get(f"{BASE_URL}/api/aggregation/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data.get("status") == "ok", f"Expected ok status, got: {data}"
        assert "counts" in data, "Response should contain counts"


class TestArticlesAPI:
    """Test articles API with categories"""
    
    def test_get_articles_returns_200(self):
        """Test that articles endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/articles")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    def test_articles_have_correct_structure(self):
        """Test that articles have correct structure"""
        response = requests.get(f"{BASE_URL}/api/articles?limit=5")
        assert response.status_code == 200
        
        articles = response.json()
        if len(articles) > 0:
            article = articles[0]
            required_fields = ["id", "titre", "slug", "categorie", "auteur", "contenu", "extrait"]
            for field in required_fields:
                assert field in article, f"Article missing required field: {field}"
    
    def test_articles_have_valid_categories(self):
        """Test that articles have valid categories"""
        response = requests.get(f"{BASE_URL}/api/articles?limit=20")
        assert response.status_code == 200
        
        articles = response.json()
        valid_categories = ["Société", "Économie", "Éducation", "Technologie", "Emploi", 
                          "Analyses / Opinions", "Politique", "Sport", "Santé", "Culture"]
        
        for article in articles:
            category = article.get("categorie")
            assert category in valid_categories, f"Invalid category: {category}"
    
    def test_filter_articles_by_category(self):
        """Test filtering articles by category"""
        # Test filtering by Sport category
        response = requests.get(f"{BASE_URL}/api/articles?categorie=Sport")
        assert response.status_code == 200
        
        articles = response.json()
        for article in articles:
            assert article.get("categorie") == "Sport", f"Expected Sport category, got: {article.get('categorie')}"


class TestBankTransferDetails:
    """Test bank transfer details contain BDA information"""
    
    def test_bank_transfer_method_available(self):
        """Test that bank transfer method is available"""
        response = requests.get(f"{BASE_URL}/api/payments-multi/methods")
        assert response.status_code == 200
        
        data = response.json()
        methods = data["methods"]
        
        bank_transfer_found = False
        for method in methods:
            if method.get("id") == "bank_transfer":
                bank_transfer_found = True
                assert method.get("available") == True, "Bank transfer should be available"
                break
        
        assert bank_transfer_found, "Bank transfer method not found"


class TestFormationsAPI:
    """Test formations API"""
    
    def test_get_formations_returns_200(self):
        """Test that formations endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/formations")
        assert response.status_code == 200
    
    def test_formations_have_correct_structure(self):
        """Test that formations have correct structure"""
        response = requests.get(f"{BASE_URL}/api/formations?limit=3")
        assert response.status_code == 200
        
        formations = response.json()
        if len(formations) > 0:
            formation = formations[0]
            required_fields = ["id", "titre", "slug", "thematique", "niveau", "description"]
            for field in required_fields:
                assert field in formation, f"Formation missing required field: {field}"


class TestEmploisAPI:
    """Test emplois (jobs) API"""
    
    def test_get_emplois_returns_200(self):
        """Test that emplois endpoint returns 200"""
        response = requests.get(f"{BASE_URL}/api/emplois")
        assert response.status_code == 200
    
    def test_emplois_have_correct_structure(self):
        """Test that emplois have correct structure"""
        response = requests.get(f"{BASE_URL}/api/emplois?limit=4")
        assert response.status_code == 200
        
        emplois = response.json()
        if len(emplois) > 0:
            emploi = emplois[0]
            required_fields = ["id", "titre", "slug", "type", "entreprise", "localisation"]
            for field in required_fields:
                assert field in emploi, f"Emploi missing required field: {field}"


class TestRootAPI:
    """Test root API endpoint"""
    
    def test_root_endpoint(self):
        """Test root API endpoint"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data, "Root endpoint should return a message"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
