import json
import requests
import pytest  # pylint: disable=E0401


# Helper for pretty printing JSON (similar to `jq .`)
def print_json(data):
    try:
        print(json.dumps(data, indent=4))
    except (TypeError, ValueError):
        print(data)  # Not JSON, print as is


# --- Global variables for test data (shared within the test module) ---
REQUEST_TIMEOUT = 5
PRODUCT_UUID = None
PRODUCT_ID = None  # Assuming ID might be different from UUID, based on script


# --- Test Functions ---

@pytest.mark.parametrize('expected_status', [200])
def test_health_check(base_url, expected_status):
    """Test 1: Health Check"""
    print("\n--- Running: Health Check ---")
    response = requests.get(f"{base_url}/health", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == expected_status


@pytest.mark.parametrize('expected_status', [200])
def test_get_all_products_empty(base_url, db_empty, expected_status):
    """Test 2: Get All Products (initially empty, only if --db-empty is true)"""
    if not db_empty:
        pytest.skip("Skipping 'Get All Products (Empty)' as --db-empty is not set.")

    print("\n--- Running: Get All Products (Empty) ---")
    response = requests.get(f"{base_url}/api/products", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == expected_status
    assert response.json() == []  # Expect an empty list if DB is truly empty


def test_create_product(base_url):
    """Test 3: Create Product"""
    global PRODUCT_UUID, PRODUCT_ID  # pylint: disable=W0603

    print("\n--- Running: Create Product ---")
    product_data = {
        "name": "Test Laptop",
        "sku": "TL-TEST-2024-001",
        "description": "High-performance test laptop",
        "quantity": 50,
        "price": 1299.99
    }
    response = requests.post(f"{base_url}/api/products", json=product_data, timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    response_json = response.json()
    print_json(response_json)

    assert response.status_code == 201

    # Extract product ID and UUID for subsequent tests
    # Using .get() for safety if key might be missing, with fallback to None
    PRODUCT_UUID = response_json.get('uuid')
    # Use 'id' if present, otherwise fall back to 'uuid'
    PRODUCT_ID = response_json.get('id', PRODUCT_UUID)

    print(f"Created Product ID: {PRODUCT_ID}")
    print(f"Created Product UUID: {PRODUCT_UUID}")

    assert PRODUCT_UUID is not None
    assert PRODUCT_ID is not None
    assert response_json.get('name') == "Test Laptop"


@pytest.mark.parametrize('expected_status', [200])
def test_get_all_products_with_data(base_url, expected_status):
    """Test 4: Get All Products (should have one product)"""
    print("\n--- Running: Get All Products (With Data) ---")
    response = requests.get(f"{base_url}/api/products", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json())
    assert response.status_code == expected_status
    assert len(response.json()) >= 1  # At least one product (the one we just created)
    # Further checks could verify the created product is in the list


def test_get_product_by_id(base_url):
    """Test 5: Get Product by ID"""
    if PRODUCT_ID is None:
        pytest.fail("Skipping Get Product by ID - no product ID available from creation test.")

    print(f"\n--- Running: Get Product by ID (ID: {PRODUCT_ID}) ---")
    response = requests.get(f"{base_url}/api/products/{PRODUCT_ID}", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json())
    assert response.status_code == 200
    assert response.json().get('uuid') == PRODUCT_UUID


@pytest.mark.parametrize("non_existent_id, expected_status", [(99999, 404)])
def test_get_product_by_non_existent_id(base_url, non_existent_id, expected_status):
    """Test 6: Get Product by Non-existent ID (404 test)"""
    print(f"\n--- Running: Get Product by Non-existent ID ({non_existent_id}) ---")
    response = requests.get(f"{base_url}/api/products/{non_existent_id}", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == expected_status


def test_update_product(base_url):
    """Test 7: Update Product"""
    if PRODUCT_ID is None:
        pytest.fail("Skipping Update Product - no product ID available from creation test.")

    print(f"\n--- Running: Update Product (ID: {PRODUCT_ID}) ---")
    updated_data = {
        "name": "Updated Test Laptop",
        "description": "Updated high-performance test laptop",
        "quantity": 45,
        "price": 1399.99
    }
    response = requests.put(f"{base_url}/api/products/{PRODUCT_ID}", json=updated_data, timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json())
    assert response.status_code == 200
    assert response.json().get('name') == "Updated Test Laptop"
    assert response.json().get('quantity') == 45


@pytest.mark.parametrize("non_existent_id, expected_status", [(99999, 404)])
def test_update_non_existent_product(base_url, non_existent_id, expected_status):
    """Test 8: Update Non-existent Product (404 test)"""
    print(f"\n--- Running: Update Non-existent Product ({non_existent_id}) ---")
    update_data = {
        "name": "Non-existent Product",
        "quantity": 10,
        "price": 100.00
    }
    response = requests.put(f"{base_url}/api/products/{non_existent_id}", json=update_data, timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == expected_status


@pytest.mark.parametrize("invalid_data, expected_status", [
    ({"name": "", "sku": "", "quantity": -1, "price": -100}, 400),
    ({"name": "No SKU", "quantity": 10}, 400)  # Assuming SKU is required
])
def test_create_product_with_invalid_data(base_url, invalid_data, expected_status):
    """Test 9: Create Product with Invalid Data (400 test)"""
    print("\n--- Running: Create Product with Invalid Data ---")
    print(f"Sending: {invalid_data}")
    response = requests.post(f"{base_url}/api/products", json=invalid_data, timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == expected_status


def test_restock_product(base_url):
    """Test 10: Restock Product"""
    if PRODUCT_ID is None:
        pytest.fail("Skipping Restock Product - no product ID available.")

    print(f"\n--- Running: Restock Product (ID: {PRODUCT_ID}) ---")
    restock_data = {
        "quantity": 25,
        "reason": "New shipment received for testing"
    }
    url = f"{base_url}/api/products/{PRODUCT_ID}/restock"
    response = requests.post(url, json=restock_data, timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json())
    assert response.status_code == 200
    assert response.json().get('quantity') == 70  # 45 (updated) + 25 (restock)


@pytest.mark.parametrize("non_existent_id, expected_status", [(99999, 404)])
def test_restock_non_existent_product(base_url, non_existent_id, expected_status):
    """Test 11: Restock Non-existent Product (404 test)"""
    print(f"\n--- Running: Restock Non-existent Product ({non_existent_id}) ---")
    restock_data = {
        "quantity": 25,
        "reason": "Test restock"
    }
    url = f"{base_url}/api/products/{non_existent_id}/restock"
    response = requests.post(url, json=restock_data, timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == expected_status


def test_restock_with_invalid_quantity(base_url):
    """Test 12: Restock with Invalid Data (400 test)"""
    if PRODUCT_ID is None:
        pytest.fail("Skipping Restock with Invalid Quantity - no product ID available.")

    print(f"\n--- Running: Restock with Invalid Quantity (ID: {PRODUCT_ID}) ---")
    invalid_restock_data = {
        "quantity": 0,  # Quantity cannot be 0 or negative for restock
        "reason": "Invalid quantity test"
    }
    url = f"{base_url}/api/products/{PRODUCT_ID}/restock"
    response = requests.post(url, json=invalid_restock_data, timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == 400


@pytest.mark.parametrize('expected_status', [200])
def test_get_restock_history(base_url, expected_status):
    """Test 13: Get Restock History"""
    print("\n--- Running: Get Restock History ---")
    response = requests.get(f"{base_url}/api/restocks", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json())
    assert response.status_code == expected_status
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1  # At least one restock if previous restock test passed


@pytest.mark.parametrize('expected_status', [200])
def test_get_low_stock_products(base_url, expected_status):
    """Test 14: Get Low Stock Products"""
    print("\n--- Running: Get Low Stock Products ---")
    response = requests.get(f"{base_url}/api/products/low-stock", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json())
    assert response.status_code == expected_status
    assert isinstance(response.json(), list)


# Test 15 was commented out in the shell script, so we'll skip it here too for consistency
# @pytest.mark.parametrize('expected_status', [200])
# def test_get_stock_analytics(base_url, expected_status):
#     """Test 15: Get Stock Analytics"""
#     print("\n--- Running: Get Stock Analytics ---")
#     response = requests.get(f"{base_url}/api/products/analytics", timeout=REQUEST_TIMEOUT)
#     print(f"Status: {response.status_code}")
#     print("Response Body:")
#     print_json(response.json())
#     assert response.status_code == expected_status

def test_delete_product(base_url):
    """Test 16: Delete Product"""
    global PRODUCT_ID  # pylint: disable=W0603
    if PRODUCT_ID is None:
        pytest.fail("Skipping Delete Product - no product ID available.")

    print(f"\n--- Running: Delete Product (ID: {PRODUCT_ID}) ---")
    response = requests.delete(f"{base_url}/api/products/{PRODUCT_ID}", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print(response.text)  # Usually empty or simple message for 204
    assert response.status_code == 204
    PRODUCT_ID = None  # Clear ID after deletion, so subsequent tests dependent on it will fail


@pytest.mark.parametrize("non_existent_id, expected_status", [(99999, 404)])
def test_delete_non_existent_product(base_url, non_existent_id, expected_status):
    """Test 17: Delete Non-existent Product (404 test)"""
    print(f"\n--- Running: Delete Non-existent Product ({non_existent_id}) ---")
    response = requests.delete(f"{base_url}/api/products/{non_existent_id}", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == expected_status


def test_verify_product_deletion(base_url):
    """Test 18: Verify Product Deletion (Should be 404)"""
    # Use the original PRODUCT_UUID if ID became None after successful deletion
    # If the API uses UUID for lookup after deletion, this is more robust
    lookup_id = PRODUCT_UUID if PRODUCT_ID is None else PRODUCT_ID

    if lookup_id is None:
        pytest.fail("Skipping Verify Product Deletion - no product ID/UUID available.")

    print(f"\n--- Running: Verify Product Deletion (ID: {lookup_id}) ---")
    response = requests.get(f"{base_url}/api/products/{lookup_id}", timeout=REQUEST_TIMEOUT)
    print(f"Status: {response.status_code}")
    print("Response Body:")
    print_json(response.json() if response.content else response.text)
    assert response.status_code == 404
