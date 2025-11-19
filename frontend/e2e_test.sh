#!/bin/bash

# E2E Test Script for GoodServices Platform
# Tests all user workflows via API endpoints

BASE_URL="http://localhost:8000/api/v1"
TIMESTAMP=$(date +%s)
TEST_RESULTS_FILE="test_results_${TIMESTAMP}.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test data
USER_A_USERNAME="testuser_a_${TIMESTAMP}"
USER_A_PASSWORD="Test123"
USER_B_USERNAME="testuser_b_${TIMESTAMP}"
USER_B_PASSWORD="Test456"

USER_A_TOKEN=""
USER_B_TOKEN=""
SERVICE_REQUEST_ID=""
SERVICE_RESPONSE_ID=""

# Function to log test results
log_test() {
    local test_name="$1"
    local status="$2"
    local details="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))

    if [ "$status" == "PASS" ]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        echo -e "${GREEN}✓ PASS${NC}: $test_name" | tee -a "$TEST_RESULTS_FILE"
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        echo -e "${RED}✗ FAIL${NC}: $test_name" | tee -a "$TEST_RESULTS_FILE"
        echo "  Details: $details" | tee -a "$TEST_RESULTS_FILE"
    fi
}

echo "========================================" | tee "$TEST_RESULTS_FILE"
echo "GoodServices E2E Test Suite" | tee -a "$TEST_RESULTS_FILE"
echo "Started at: $(date)" | tee -a "$TEST_RESULTS_FILE"
echo "========================================" | tee -a "$TEST_RESULTS_FILE"
echo "" | tee -a "$TEST_RESULTS_FILE"

#############################################
# Test 1: User Registration (User A)
#############################################
echo -e "${YELLOW}[1] Testing User Registration (User A)${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"uname\": \"$USER_A_USERNAME\",
    \"bname\": \"Test User A\",
    \"ctype\": \"身份证\",
    \"idno\": \"110101199001011234\",
    \"bpwd\": \"$USER_A_PASSWORD\",
    \"phoneNo\": \"13800138001\",
    \"desc\": \"Test user A for E2E testing\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "201" ]; then
    log_test "User A registration" "PASS" ""
else
    log_test "User A registration" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 2: User Registration (User B)
#############################################
echo -e "${YELLOW}[2] Testing User Registration (User B)${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"uname\": \"$USER_B_USERNAME\",
    \"bname\": \"Test User B\",
    \"ctype\": \"身份证\",
    \"idno\": \"110101199002022345\",
    \"bpwd\": \"$USER_B_PASSWORD\",
    \"phoneNo\": \"13800138002\",
    \"desc\": \"Test user B for E2E testing\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "201" ]; then
    log_test "User B registration" "PASS" ""
else
    log_test "User B registration" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 3: Password Validation (Weak Password)
#############################################
echo -e "${YELLOW}[3] Testing Weak Password Validation${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"uname\": \"weakpwd_${TIMESTAMP}\",
    \"bname\": \"Weak Password User\",
    \"ctype\": \"身份证\",
    \"idno\": \"110101199003033456\",
    \"bpwd\": \"weak\",
    \"phoneNo\": \"13800138003\",
    \"desc\": \"Test weak password\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "422" ]; then
    log_test "Weak password validation" "PASS" ""
else
    log_test "Weak password validation" "FAIL" "Expected 422, got HTTP $HTTP_CODE"
fi

#############################################
# Test 4: User Login (User A)
#############################################
echo -e "${YELLOW}[4] Testing User Login (User A)${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$USER_A_USERNAME\",
    \"password\": \"$USER_A_PASSWORD\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    USER_A_TOKEN=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    if [ -n "$USER_A_TOKEN" ]; then
        log_test "User A login" "PASS" ""
    else
        log_test "User A login" "FAIL" "No access token in response"
    fi
else
    log_test "User A login" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 5: User Login (User B)
#############################################
echo -e "${YELLOW}[5] Testing User Login (User B)${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$USER_B_USERNAME\",
    \"password\": \"$USER_B_PASSWORD\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    USER_B_TOKEN=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    if [ -n "$USER_B_TOKEN" ]; then
        log_test "User B login" "PASS" ""
    else
        log_test "User B login" "FAIL" "No access token in response"
    fi
else
    log_test "User B login" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 6: Invalid Credentials
#############################################
echo -e "${YELLOW}[6] Testing Invalid Login Credentials${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"uname\": \"wronguser\",
    \"bpwd\": \"WrongPass123\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "401" ]; then
    log_test "Invalid credentials rejection" "PASS" ""
else
    log_test "Invalid credentials rejection" "FAIL" "Expected 401, got HTTP $HTTP_CODE"
fi

#############################################
# Test 7: Get Current User Info (User A)
#############################################
echo -e "${YELLOW}[7] Testing Get Current User Info${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/users/me" \
  -H "Authorization: Bearer $USER_A_TOKEN")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    USERNAME=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['uname'])" 2>/dev/null)
    if [ "$USERNAME" == "$USER_A_USERNAME" ]; then
        log_test "Get current user info" "PASS" ""
    else
        log_test "Get current user info" "FAIL" "Wrong username returned"
    fi
else
    log_test "Get current user info" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 8: Publish Service Request (User A)
#############################################
echo -e "${YELLOW}[8] Testing Publish Service Request${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/service-requests" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"ps_title\": \"Kitchen plumbing repair needed\",
    \"ps_desc\": \"Kitchen sink is leaking badly, need immediate repair\",
    \"stype_id\": 1,
    \"cityID\": 1,
    \"begin_date\": \"2025-12-15\",
    \"end_date\": \"2025-12-16\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "201" ]; then
    SERVICE_REQUEST_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['psid'])" 2>/dev/null)
    if [ -n "$SERVICE_REQUEST_ID" ]; then
        log_test "Publish service request" "PASS" "Request ID: $SERVICE_REQUEST_ID"
    else
        log_test "Publish service request" "FAIL" "No request ID in response"
    fi
else
    log_test "Publish service request" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 9: Get My Service Requests (User A)
#############################################
echo -e "${YELLOW}[9] Testing Get My Service Requests${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/service-requests/my" \
  -H "Authorization: Bearer $USER_A_TOKEN")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    COUNT=$(echo "$BODY" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['items']))" 2>/dev/null)
    if [ "$COUNT" -ge 1 ]; then
        log_test "Get my service requests" "PASS" "Found $COUNT request(s)"
    else
        log_test "Get my service requests" "FAIL" "No requests found"
    fi
else
    log_test "Get my service requests" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 10: Browse Service Requests (User B)
#############################################
echo -e "${YELLOW}[10] Testing Browse Service Requests (User B)${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/service-requests" \
  -H "Authorization: Bearer $USER_B_TOKEN")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    COUNT=$(echo "$BODY" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['items']))" 2>/dev/null)
    if [ "$COUNT" -ge 1 ]; then
        log_test "Browse service requests" "PASS" "Found $COUNT request(s)"
    else
        log_test "Browse service requests" "FAIL" "No requests found"
    fi
else
    log_test "Browse service requests" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 11: Submit Service Response (User B)
#############################################
echo -e "${YELLOW}[11] Testing Submit Service Response (User B)${NC}" | tee -a "$TEST_RESULTS_FILE"

if [ -n "$SERVICE_REQUEST_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/service-responses" \
      -H "Authorization: Bearer $USER_B_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"srid\": $SERVICE_REQUEST_ID,
        \"response_desc\": \"Professional plumber available. 10 years experience. Can fix within 1 hour.\"
      }")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)

    if [ "$HTTP_CODE" == "201" ]; then
        SERVICE_RESPONSE_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['response_id'])" 2>/dev/null)
        if [ -n "$SERVICE_RESPONSE_ID" ]; then
            log_test "Submit service response" "PASS" "Response ID: $SERVICE_RESPONSE_ID"
        else
            log_test "Submit service response" "FAIL" "No response ID in response"
        fi
    else
        log_test "Submit service response" "FAIL" "HTTP $HTTP_CODE: $BODY"
    fi
else
    log_test "Submit service response" "SKIP" "No service request ID available"
fi

#############################################
# Test 12: Get My Service Responses (User B)
#############################################
echo -e "${YELLOW}[12] Testing Get My Service Responses (User B)${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/service-responses/my" \
  -H "Authorization: Bearer $USER_B_TOKEN")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    COUNT=$(echo "$BODY" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['items']))" 2>/dev/null)
    if [ "$COUNT" -ge 1 ]; then
        log_test "Get my service responses" "PASS" "Found $COUNT response(s)"
    else
        log_test "Get my service responses" "FAIL" "No responses found"
    fi
else
    log_test "Get my service responses" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 13: Accept Service Response (User A)
#############################################
echo -e "${YELLOW}[13] Testing Accept Service Response (User A)${NC}" | tee -a "$TEST_RESULTS_FILE"

if [ -n "$SERVICE_RESPONSE_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/match/accept/$SERVICE_RESPONSE_ID" \
      -H "Authorization: Bearer $USER_A_TOKEN")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)

    if [ "$HTTP_CODE" == "200" ]; then
        log_test "Accept service response" "PASS" ""
    else
        log_test "Accept service response" "FAIL" "HTTP $HTTP_CODE: $BODY"
    fi
else
    log_test "Accept service response" "SKIP" "No service response ID available"
fi

#############################################
# Test 14: Verify Response State Changed to Accepted
#############################################
echo -e "${YELLOW}[14] Testing Response State After Acceptance${NC}" | tee -a "$TEST_RESULTS_FILE"

if [ -n "$SERVICE_RESPONSE_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/service-responses/$SERVICE_RESPONSE_ID" \
      -H "Authorization: Bearer $USER_A_TOKEN")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)

    if [ "$HTTP_CODE" == "200" ]; then
        STATE=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['response_state'])" 2>/dev/null)
        if [ "$STATE" == "1" ]; then
            log_test "Response state changed to accepted" "PASS" ""
        else
            log_test "Response state changed to accepted" "FAIL" "State is $STATE, expected 1"
        fi
    else
        log_test "Response state changed to accepted" "FAIL" "HTTP $HTTP_CODE: $BODY"
    fi
else
    log_test "Response state changed to accepted" "SKIP" "No service response ID available"
fi

#############################################
# Test 15: Cancel Service Request
#############################################
echo -e "${YELLOW}[15] Testing Cancel Service Request${NC}" | tee -a "$TEST_RESULTS_FILE"

# Create a new request to cancel
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/service-requests" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"ps_title\": \"Test request to cancel\",
    \"ps_desc\": \"This request will be cancelled\",
    \"stype_id\": 2,
    \"cityID\": 1,
    \"begin_date\": \"2025-12-20\",
    \"end_date\": \"2025-12-21\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "201" ]; then
    CANCEL_REQUEST_ID=$(echo "$BODY" | python3 -c "import sys, json; print(json.load(sys.stdin)['psid'])" 2>/dev/null)

    # Now cancel it
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/service-requests/$CANCEL_REQUEST_ID/cancel" \
      -H "Authorization: Bearer $USER_A_TOKEN")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

    if [ "$HTTP_CODE" == "200" ]; then
        log_test "Cancel service request" "PASS" ""
    else
        log_test "Cancel service request" "FAIL" "HTTP $HTTP_CODE"
    fi
else
    log_test "Cancel service request" "SKIP" "Could not create test request"
fi

#############################################
# Test 16: Unauthorized Access (User B tries to edit User A's request)
#############################################
echo -e "${YELLOW}[16] Testing Authorization Check${NC}" | tee -a "$TEST_RESULTS_FILE"

if [ -n "$SERVICE_REQUEST_ID" ]; then
    RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/service-requests/$SERVICE_REQUEST_ID" \
      -H "Authorization: Bearer $USER_B_TOKEN" \
      -H "Content-Type: application/json" \
      -d "{
        \"ps_title\": \"Unauthorized edit attempt\",
        \"ps_desc\": \"This should fail\",
        \"stype_id\": 1,
        \"cityID\": 1,
        \"begin_date\": \"2025-12-15\",
        \"end_date\": \"2025-12-16\"
      }")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

    if [ "$HTTP_CODE" == "403" ] || [ "$HTTP_CODE" == "401" ]; then
        log_test "Authorization check (prevent unauthorized edit)" "PASS" ""
    else
        log_test "Authorization check (prevent unauthorized edit)" "FAIL" "Expected 403/401, got HTTP $HTTP_CODE"
    fi
else
    log_test "Authorization check" "SKIP" "No service request ID available"
fi

#############################################
# Test 17: Statistics API
#############################################
echo -e "${YELLOW}[17] Testing Statistics Dashboard API${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/stats/monthly?start_month=2025-01&end_month=2025-12" \
  -H "Authorization: Bearer $USER_A_TOKEN")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    log_test "Statistics dashboard API" "PASS" ""
else
    log_test "Statistics dashboard API" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test 18: Statistics with City Filter
#############################################
echo -e "${YELLOW}[18] Testing Statistics with City Filter${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/stats/monthly?start_month=2025-01&end_month=2025-12&city_id=1" \
  -H "Authorization: Bearer $USER_A_TOKEN")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "200" ]; then
    log_test "Statistics with city filter" "PASS" ""
else
    log_test "Statistics with city filter" "FAIL" "HTTP $HTTP_CODE"
fi

#############################################
# Test 19: Statistics with Service Type Filter
#############################################
echo -e "${YELLOW}[19] Testing Statistics with Service Type Filter${NC}" | tee -a "$TEST_RESULTS_FILE"

RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/stats/monthly?start_month=2025-01&end_month=2025-12&service_type_id=1" \
  -H "Authorization: Bearer $USER_A_TOKEN")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

if [ "$HTTP_CODE" == "200" ]; then
    log_test "Statistics with service type filter" "PASS" ""
else
    log_test "Statistics with service type filter" "FAIL" "HTTP $HTTP_CODE"
fi

#############################################
# Test 20: Password Change
#############################################
echo -e "${YELLOW}[20] Testing Password Change${NC}" | tee -a "$TEST_RESULTS_FILE"

NEW_PASSWORD="NewPass456"

RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/users/me/password" \
  -H "Authorization: Bearer $USER_A_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"old_password\": \"$USER_A_PASSWORD\",
    \"new_password\": \"$NEW_PASSWORD\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" == "200" ]; then
    # Try logging in with new password
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/auth/login" \
      -H "Content-Type: application/json" \
      -d "{
        \"uname\": \"$USER_A_USERNAME\",
        \"bpwd\": \"$NEW_PASSWORD\"
      }")

    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)

    if [ "$HTTP_CODE" == "200" ]; then
        log_test "Password change" "PASS" ""
    else
        log_test "Password change" "FAIL" "Login with new password failed"
    fi
else
    log_test "Password change" "FAIL" "HTTP $HTTP_CODE: $BODY"
fi

#############################################
# Test Summary
#############################################
echo "" | tee -a "$TEST_RESULTS_FILE"
echo "========================================" | tee -a "$TEST_RESULTS_FILE"
echo "Test Summary" | tee -a "$TEST_RESULTS_FILE"
echo "========================================" | tee -a "$TEST_RESULTS_FILE"
echo "Total Tests: $TOTAL_TESTS" | tee -a "$TEST_RESULTS_FILE"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}" | tee -a "$TEST_RESULTS_FILE"
echo -e "${RED}Failed: $FAILED_TESTS${NC}" | tee -a "$TEST_RESULTS_FILE"
echo "Completed at: $(date)" | tee -a "$TEST_RESULTS_FILE"
echo "========================================" | tee -a "$TEST_RESULTS_FILE"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}" | tee -a "$TEST_RESULTS_FILE"
    exit 0
else
    echo -e "${RED}Some tests failed. Check details above.${NC}" | tee -a "$TEST_RESULTS_FILE"
    exit 1
fi
