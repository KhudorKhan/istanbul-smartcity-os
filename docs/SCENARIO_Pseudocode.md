# Scenario: Paying for Parking Using Cryptocurrency

## Scenario Description

A resident user wants to pay for parking using Ethereum cryptocurrency. The system must authenticate the user, validate the payment, process it through the Ethereum adapter, create a transaction record, notify the user, and log the event for audit purposes.

## Detailed Scenario Flow

### Actors

- **Resident**: Jack (username: "jack_smith")
- **System**: DigiBank Payment System
- **Ethereum Network**: External blockchain network

### Preconditions

1. User "jack_smith" is registered in the system
2. User has sufficient Ethereum balance in their account
3. User is authenticated with a valid JWT token
4. Parking service is available

### Main Flow

````
1. User initiates payment request
   - User sends POST request to /api/pay/crypto
   - Headers: Authorization: Bearer <JWT_TOKEN>
   - Body: {
       "paymentType": "CRYPTO",
       "amount": 0.05,
       "cryptoNetwork": "ETH",
       "serviceType": "PARKING",
       "description": "Parking fee - Zone A, 2 hours"
     }

2. System validates authentication
   - Extract JWT token from Authorization header
   - Validate token signature and expiration
   - Extract user information from token
   - User: jack_smith (ID: 123)

3. System retrieves user account
   - Query AccountRepository for user ID 123
   - Account found: fiatBalance = $100.00, cryptoBalance = 0.5 ETH

4. Command Pattern: Create CryptoPaymentCommand
   - Command created with:
     * paymentService reference
     * user: jack_smith
     * account: Account{id: 456}
     * amount: 0.05 ETH
     * cryptoNetwork: "ETH"
     * serviceType: PARKING
     * description: "Parking fee - Zone A, 2 hours"

5. Command Pattern: Check if payment can execute
   - canExecute() called
   - Check: account.cryptoBalance (0.5) >= amount (0.05)
   - Result: TRUE - payment can proceed

6. Template Method Pattern: Security Check
   - performSecurityCheck(user, amount) called
   - Step 1: validateUser(user)
     * Check: user != null && username not empty
     * Result: TRUE
   - Step 2: checkAccountStatus(user)
     * Check: user.role != null
     * Result: TRUE
   - Step 3: validateAmount(amount)
     * Check: amount >= 0.01 && amount <= 10000
     * Result: TRUE (0.05 is valid)
   - Step 4: performCustomChecks(user, amount)
     * Additional security validations
     * Result: TRUE
   - Overall Result: Security check PASSED

7. Adapter Pattern: Process crypto payment
   - CryptoAdapterFactory.getAdapter("ETH") called
   - EthereumAdapter instance created
   - adapter.processPayment(walletAddress, 0.05, "ETH") called
   - Simulated transaction hash generated: "0x1234567890eth"
   - Transaction hash returned: "0x1234567890eth"

8. Update account balance
   - account.cryptoBalance = 0.5 - 0.05 = 0.45 ETH
   - AccountRepository.save(account) called
   - Database updated

9. Create transaction record
   - Transaction object created:
     * user: jack_smith
     * paymentType: CRYPTO
     * serviceType: PARKING
     * amount: 0.05
     * status: COMPLETED
     * cryptoNetwork: "ETH"
     * transactionHash: "0x1234567890eth"
     * description: "Parking fee - Zone A, 2 hours"
   - TransactionRepository.save(transaction) called
   - Transaction ID: 789 created

10. Singleton Pattern: Update city metrics
    - CityController.getInstance() called
    - controller.incrementTransactionCount() called
    - controller.addRevenue(0.05) called
    - System metrics updated

11. Observer Pattern: Notify observers
    - NotificationSubject.notifyObservers(transaction) called
    - For each observer in observers list:
      a. EmailNotificationObserver.update(transaction)
         * Log: "📧 Email Notification: Transaction 789: CRYPTO payment of 0.05 for PARKING - Status: COMPLETED"
      b. SecurityAlertObserver.update(transaction)
         * Check: transaction.status == FAILED?
         * Result: FALSE (status is COMPLETED)
         * No security alert triggered

12. Audit logging
    - AuditService.logPayment(123, "CRYPTO", 0.05, PARKING) called
    - AuditLog created:
      * userId: 123
      * eventType: PAYMENT
      * action: "PAYMENT_PROCESSED"
      * details: "Payment: CRYPTO, Amount: 0.05, Service: PARKING"
    - AuditLogRepository.save(log) called

13. Return response to user
    - HTTP 200 OK
    - Body: {
        "success": true,
        "message": "Crypto payment processed",
        "data": {
          "id": 789,
          "paymentType": "CRYPTO",
          "serviceType": "PARKING",
          "amount": 0.05,
          "status": "COMPLETED",
          "cryptoNetwork": "ETH",
          "transactionHash": "0x1234567890eth",
          "timestamp": "2024-01-15T10:30:00"
        }
      }

### Postconditions
1. User's crypto balance reduced by 0.05 ETH
2. Transaction record created with status COMPLETED
3. City controller metrics updated
4. Email notification sent (simulated)
5. Audit log entry created
6. Parking service notified (external system)

## Pseudocode

```pseudocode
FUNCTION processCryptoParkingPayment(userToken, paymentRequest):
    // Step 1: Authentication
    user = validateJWTToken(userToken)
    IF user IS NULL:
        RETURN ERROR("Invalid token")
    END IF

    // Step 2: Retrieve account
    account = accountRepository.findByUserId(user.id)
    IF account IS NULL:
        RETURN ERROR("Account not found")
    END IF

    // Step 3: Create command (Command Pattern)
    command = NEW CryptoPaymentCommand(
        paymentService, user, account,
        paymentRequest.amount,
        paymentRequest.cryptoNetwork,
        PARKING,
        paymentRequest.description
    )

    // Step 4: Validate command
    IF NOT command.canExecute():
        RETURN ERROR("Insufficient balance")
    END IF

    // Step 5: Security check (Template Method Pattern)
    securityCheck = NEW PaymentSecurityCheck()
    IF NOT securityCheck.performSecurityCheck(user, paymentRequest.amount):
        RETURN ERROR("Security check failed")
    END IF

    // Step 6: Process payment via adapter (Adapter Pattern)
    adapter = CryptoAdapterFactory.getAdapter(paymentRequest.cryptoNetwork)
    walletAddress = "user_" + user.id + "_wallet"
    transactionHash = adapter.processPayment(
        walletAddress,
        paymentRequest.amount,
        paymentRequest.cryptoNetwork
    )

    // Step 7: Update account
    account.cryptoBalance = account.cryptoBalance - paymentRequest.amount
    accountRepository.save(account)

    // Step 8: Create transaction
    transaction = NEW Transaction()
    transaction.user = user
    transaction.paymentType = CRYPTO
    transaction.serviceType = PARKING
    transaction.amount = paymentRequest.amount
    transaction.status = COMPLETED
    transaction.cryptoNetwork = paymentRequest.cryptoNetwork
    transaction.transactionHash = transactionHash
    transaction.description = paymentRequest.description
    transaction = transactionRepository.save(transaction)

    // Step 9: Update metrics (Singleton Pattern)
    cityController = CityController.getInstance()
    cityController.incrementTransactionCount()
    cityController.addRevenue(paymentRequest.amount)

    // Step 10: Notify observers (Observer Pattern)
    notificationSubject.notifyObservers(transaction)

    // Step 11: Audit logging
    auditService.logPayment(
        user.id,
        "CRYPTO",
        paymentRequest.amount,
        PARKING
    )

    // Step 12: Return success
    RETURN SUCCESS(transaction)
END FUNCTION
````

## Design Patterns Demonstrated

1. **Command Pattern**: `CryptoPaymentCommand` encapsulates the payment request
2. **Adapter Pattern**: `EthereumAdapter` adapts the Ethereum network interface
3. **Template Method Pattern**: `SecurityCheckTemplate` defines the security check algorithm
4. **Observer Pattern**: `NotificationSubject` notifies `EmailNotificationObserver` and `SecurityAlertObserver`
5. **Singleton Pattern**: `CityController.getInstance()` provides single instance for metrics

## Error Handling

- **Insufficient Balance**: Command.canExecute() returns false → HTTP 400
- **Security Check Failure**: SecurityCheckTemplate returns false → HTTP 400
- **Invalid Token**: JWT validation fails → HTTP 401
- **Network Error**: Adapter fails → Transaction status = FAILED, Observer notified
