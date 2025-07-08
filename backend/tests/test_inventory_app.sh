#!/bin/bash

# Inventory API Test Suite
# Usage: ./test_inventory_api.sh <BASE_URL> [DB_EMPTY]
# <BASE_URL>: The base URL of the inventory API (e.g., http://localhost:8085)
# [DB_EMPTY]: Optional. Set to 'true' to run tests for empty DB. Default is 'false'.

set -e

# Configuration
BASE_URL=""
DB_EMPTY="false" # Default to not running tests for empty DB

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0

# Helper functions
log_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
    echo ""
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED_TESTS++))
    echo ""
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
    echo ""
}

# Usage function
usage() {
    echo "Usage: $0 <BASE_URL> [DB_EMPTY]"
    echo "  <BASE_URL>: The base URL of the inventory API (e.g., http://localhost:8085)"
    echo "  [DB_EMPTY]: Optional. Set to 'true' to run tests for empty DB. Default is 'false'."
    exit 1
}

# Parse arguments
if [ -z "$1" ]; then
    log_error "Error: BASE_URL is required."
    usage
fi

BASE_URL="$1"

if [ -n "$2" ]; then
    if [[ "$2" == "true" ]]; then
        DB_EMPTY="true"
    fi
fi

CONTENT_TYPE="Content-Type: application/json"

run_test() {
#    echo "-1---------------------------------------"
    local test_name="$1"
    local expected_status="$2"
    local response
    local status_code

#    echo "-2---------------------------------------"
    ((TOTAL_TESTS++))
    log_info "Running: $test_name"
#    echo "-3---------------------------------------"

    # Execute the curl command and capture both response and status code
    response=$(curl -s -w "\n%{http_code}" "${@:3}")
#    echo "-4---------------------------------------"
    status_code=$(echo "$response" | tail -n1)
#    echo "-5---------------------------------------"
    body=$(echo "$response" | sed '$d')
#    echo "-6---------------------------------------"

    if [ "$status_code" -eq "$expected_status" ]; then
        log_success "$test_name (Status: $status_code)"
        # echo "- $test_name : [$PASSED_TESTS/$TOTAL_TESTS] (Status: $status_code) -"
        # echo ""
        echo "$body" | jq . 2>/dev/null || echo "$body"
    else
        log_error "$test_name (Expected: $expected_status, Got: $status_code)"
        # echo ""
        echo "$body"
    fi

    echo "----------------------------------------"
}

# Global variables for test data
PRODUCT_ID=""
PRODUCT_UUID=""

echo "Starting Inventory API Tests..."
echo "Base URL:               $BASE_URL"
echo "Run tests for empty DB: $DB_EMPTY"
echo "========================================"

# Test 1: Health Check
run_test "Health Check" 200 \
    -X GET "$BASE_URL/health"

# Test 2: Get All Products (initially empty)
if [ "$DB_EMPTY" == "true" ]; then
    run_test "Get All Products (Empty)" 200 \
        -X GET "$BASE_URL/api/products"
else
    log_info "Skipping Test 2: Get All Products (Empty) as DB_EMPTY is not 'true'."
    echo "----------------------------------------"
fi

# Test 3: Create Product
log_info "Creating test product..."
response=$(curl -s -w "\n%{http_code}" \
    -X POST "$BASE_URL/api/products" \
    -H "$CONTENT_TYPE" \
    -d '{
        "name": "Test Laptop",
        "sku": "TL-TEST-2024-001",
        "description": "High-performance test laptop",
        "quantity": 50,
        "price": 1299.99
    }')

status_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')
((TOTAL_TESTS++))

if [ "$status_code" -eq 201 ]; then
    log_success "Create Product (Status: $status_code)"
    echo "$body" | jq .

    # Extract product ID and UUID for subsequent tests
    PRODUCT_UUID=$(echo "$body" | jq -r '.uuid')
    # Assuming the API returns an ID field - if not, we'll use UUID
    PRODUCT_ID=$(echo "$body" | jq -r '.id // .uuid')

    echo "Created Product ID: $PRODUCT_ID"
    echo "Created Product UUID: $PRODUCT_UUID"
else
    log_error "Create Product (Expected: 201, Got: $status_code)"
    echo "$body"
fi

# Test 4: Get All Products (should have one product)
run_test "Get All Products (With Data)" 200 \
    -X GET "$BASE_URL/api/products"

# Test 5: Get Product by ID
if [ -n "$PRODUCT_ID" ]; then
    run_test "Get Product by ID" 200 \
        -X GET "$BASE_URL/api/products/$PRODUCT_ID"
else
    log_error "Skipping Get Product by ID - no product ID available"
fi

# Test 6: Get Product by Non-existent ID (404 test)
run_test "Get Product by Non-existent ID" 404 \
    -X GET "$BASE_URL/api/products/99999"

# Test 7: Update Product
if [ -n "$PRODUCT_ID" ]; then
    run_test "Update Product" 200 \
        -X PUT "$BASE_URL/api/products/$PRODUCT_ID" \
        -H "$CONTENT_TYPE" \
        -d '{
            "name": "Updated Test Laptop",
            "description": "Updated high-performance test laptop",
            "quantity": 45,
            "price": 1399.99
        }'
else
    log_error "Skipping Update Product - no product ID available"
fi

# Test 8: Update Non-existent Product (404 test)
run_test "Update Non-existent Product" 404 \
    -X PUT "$BASE_URL/api/products/99999" \
    -H "$CONTENT_TYPE" \
    -d '{
        "name": "Non-existent Product",
        "quantity": 10,
        "price": 100.00
    }'

# Test 9: Create Product with Invalid Data (400 test)
run_test "Create Product with Invalid Data" 400 \
    -X POST "$BASE_URL/api/products" \
    -H "$CONTENT_TYPE" \
    -d '{
        "name": "",
        "sku": "",
        "quantity": -1,
        "price": -100
    }'

# Test 10: Restock Product
if [ -n "$PRODUCT_ID" ]; then
    run_test "Restock Product" 200 \
        -X POST "$BASE_URL/api/products/$PRODUCT_ID/restock" \
        -H "$CONTENT_TYPE" \
        -d '{
            "quantity": 25,
            "reason": "New shipment received for testing"
        }'
else
    log_error "Skipping Restock Product - no product ID available"
fi

# Test 11: Restock Non-existent Product (404 test)
run_test "Restock Non-existent Product" 404 \
    -X POST "$BASE_URL/api/products/99999/restock" \
    -H "$CONTENT_TYPE" \
    -d '{
        "quantity": 25,
        "reason": "Test restock"
    }'

# Test 12: Restock with Invalid Data (400 test)
if [ -n "$PRODUCT_ID" ]; then
    run_test "Restock with Invalid Quantity" 400 \
        -X POST "$BASE_URL/api/products/$PRODUCT_ID/restock" \
        -H "$CONTENT_TYPE" \
        -d '{
            "quantity": 0,
            "reason": "Invalid quantity test"
        }'
else
    log_error "Skipping Restock with Invalid Data - no product ID available"
fi

# Test 13: Get Restock History
run_test "Get Restock History" 200 \
    -X GET "$BASE_URL/api/restocks"

# Test 14: Get Low Stock Products
run_test "Get Low Stock Products" 200 \
    -X GET "$BASE_URL/api/products/low-stock"

# Test 15: Get Stock Analytics
#run_test "Get Stock Analytics" 200 \
#    -X GET "$BASE_URL/api/products/analytics"

# Test 16: Delete Product
if [ -n "$PRODUCT_ID" ]; then
    run_test "Delete Product" 204 \
        -X DELETE "$BASE_URL/api/products/$PRODUCT_ID"
else
    log_error "Skipping Delete Product - no product ID available"
fi

# Test 17: Delete Non-existent Product (404 test)
run_test "Delete Non-existent Product" 404 \
    -X DELETE "$BASE_URL/api/products/99999"

# Test 18: Verify Product Deletion
if [ -n "$PRODUCT_ID" ]; then
    run_test "Verify Product Deletion (Should be 404)" 404 \
        -X GET "$BASE_URL/api/products/$PRODUCT_ID"
else
    log_error "Skipping Verify Product Deletion - no product ID available"
fi

# Test Summary
echo "========================================"
echo "TEST SUMMARY"
echo "========================================"
echo "Total Tests: $TOTAL_TESTS"
echo "Passed Tests: $PASSED_TESTS"
echo "Failed Tests: $((TOTAL_TESTS - PASSED_TESTS))"

if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi