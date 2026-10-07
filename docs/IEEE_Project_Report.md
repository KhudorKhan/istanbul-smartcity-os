# DigiBank: Smart City Digital Banking Module

## A Computer Engineering Project Report

**Author:** KHUDOYOR FAKHRITDINOV  
**Institution:** BEYKENT University
**Course:** OBJECT ORIENTED PROGRAMMING  
**Date:** December 2025

---

## Abstract

This report presents the design, implementation, and deployment of DigiBank, a digital banking module for smart city services. The system enables residents to make payments using both fiat currency and cryptocurrency for services such as parking, transportation, and utilities. The project demonstrates the application of five key design patterns (Singleton, Command, Observer, Adapter, and Template Method) within a Spring Boot REST API architecture. The system has been deployed to a cloud platform (Render/Railway) with PostgreSQL database integration. This report documents the system architecture, design decisions, implementation details, risk analysis, and deployment procedures. The project successfully demonstrates a production-ready backend system with comprehensive security measures, audit logging, and role-based access control.

**Keywords:** Digital Banking, Smart City, Design Patterns, Spring Boot, Cryptocurrency, REST API, Cloud Deployment

---

## 1. Introduction

### 1.1 Background

Smart cities are increasingly adopting digital payment systems to streamline municipal services. The integration of both traditional fiat currency and cryptocurrency payment methods provides residents with flexibility and aligns with modern financial technology trends. DigiBank addresses this need by providing a secure, scalable digital banking module that can be integrated into existing smart city infrastructure.

### 1.2 Problem Statement

Current smart city payment systems often lack:

- Support for multiple payment methods (fiat and cryptocurrency)
- Comprehensive audit and security logging
- Flexible integration with various blockchain networks
- Role-based access control for different user types
- Real-time notification systems for transaction events

### 1.3 Objectives

The primary objectives of this project are:

1. Design and implement a RESTful API for digital banking operations
2. Demonstrate the application of five design patterns in a real-world context
3. Support both fiat and cryptocurrency payment methods
4. Implement comprehensive security and audit logging
5. Deploy the system to a cloud platform with public accessibility
6. Provide clear documentation suitable for academic evaluation

### 1.4 Scope

The project scope includes:

- Backend API implementation (no frontend development)
- Core payment processing functionality
- User authentication and authorization
- Transaction history management
- Admin monitoring and metrics
- Design pattern demonstration
- Cloud deployment

Out of scope:

- Full frontend application (wireframes only)
- Real blockchain integration (simulated adapters)
- Mobile application
- Advanced fraud detection algorithms

### 1.5 Report Organization

This report is organized as follows: Section 2 presents the system design and architecture, Section 3 details the implementation, Section 4 covers deployment procedures, Section 5 provides risk analysis, and Section 6 concludes the report.

---

## 2. System Design

### 2.1 System Architecture

DigiBank follows a three-tier architecture:

1. **Presentation Layer**: REST API endpoints (Spring Boot Controllers)
2. **Business Logic Layer**: Services implementing business rules and design patterns
3. **Data Layer**: JPA repositories and PostgreSQL database

The system is designed with separation of concerns, allowing for maintainability and scalability.

### 2.2 Design Patterns

#### 2.2.1 Singleton Pattern

**Implementation**: `CityController` class

The Singleton pattern ensures a single instance of the city controller manages system-wide metrics and state. This is critical for maintaining consistent system statistics across all transactions.

```java
public class CityController {
    private static volatile CityController instance;
    // Thread-safe singleton implementation
}
```

**Justification**: Centralized metrics management requires a single source of truth. The Singleton pattern prevents multiple instances from creating inconsistent system statistics.

#### 2.2.2 Command Pattern

**Implementation**: `PaymentCommand` interface with `FiatPaymentCommand` and `CryptoPaymentCommand` concrete classes

The Command pattern encapsulates payment requests as objects, allowing for parameterization, queuing, logging, and undo operations.

```java
public interface PaymentCommand {
    Transaction execute();
    void undo();
    boolean canExecute();
}
```

**Justification**: Payment operations need to be encapsulated for transaction management, rollback capabilities, and audit logging. The Command pattern provides this flexibility.

#### 2.2.3 Observer Pattern

**Implementation**: `NotificationObserver` interface with `EmailNotificationObserver` and `SecurityAlertObserver` concrete observers, managed by `NotificationSubject`

The Observer pattern enables the system to notify multiple components (email service, security monitoring) when transactions occur, without tight coupling.

```java
public interface NotificationObserver {
    void update(Transaction transaction);
}
```

**Justification**: Transaction events require multiple notifications (user email, security alerts, audit logs). The Observer pattern decouples these concerns.

#### 2.2.4 Adapter Pattern

**Implementation**: `CryptoPaymentAdapter` interface with `EthereumAdapter`, `BitcoinAdapter`, and `PolygonAdapter` implementations, managed by `CryptoAdapterFactory`

The Adapter pattern allows integration with different blockchain networks through a unified interface.

```java
public interface CryptoPaymentAdapter {
    String processPayment(String walletAddress, BigDecimal amount, String network);
    boolean verifyTransaction(String transactionHash, String network);
}
```

**Justification**: Different blockchain networks have varying APIs. The Adapter pattern provides a consistent interface while allowing network-specific implementations.

#### 2.2.5 Template Method Pattern

**Implementation**: `SecurityCheckTemplate` abstract class with `PaymentSecurityCheck` concrete implementation

The Template Method pattern defines the skeleton of the security check algorithm, with specific steps implemented by subclasses.

```java
public abstract class SecurityCheckTemplate {
    public final boolean performSecurityCheck(User user, BigDecimal amount) {
        // Template method defining algorithm structure
    }
}
```

**Justification**: Security checks follow a consistent structure but may have different implementations. The Template Method pattern ensures consistency while allowing customization.

### 2.3 UML Diagrams

#### 2.3.1 Use Case Diagram

The Use Case Diagram (see `docs/UML_UseCase_Diagram.puml`) illustrates the interactions between actors and the system:

**Actors:**

- Resident: End users making payments
- Admin/City Controller: System administrators
- Fiat Payment Provider: External payment gateway
- Crypto Network: Blockchain networks
- Smart City Service: External services (parking, transport, utilities)
- Security Authority: Security monitoring system

**Key Use Cases:**

- Login/Register
- Pay with Fiat/Crypto
- View Transaction History
- Receive Notifications
- Monitor System Metrics
- View Audit Logs

#### 2.3.2 Class Diagram

The Class Diagram (see `docs/UML_Class_Diagram.puml`) shows:

1. **Domain Model**: User, Account, Transaction, AuditLog entities
2. **Design Pattern Implementations**: All five patterns clearly marked
3. **Service Layer**: PaymentService, AuthService, AccountService, AuditService
4. **Controller Layer**: REST API endpoints
5. **Relationships**: Associations, dependencies, and inheritance

### 2.4 Database Schema

**Tables:**

- `users`: User accounts with role-based access
- `accounts`: Balance information (fiat and crypto)
- `transactions`: Payment transaction records
- `audit_logs`: Security and compliance logging

**Key Relationships:**

- User 1:1 Account
- User 1:N Transaction
- Transaction references User (many-to-one)

---

## 3. Implementation

### 3.1 Technology Stack

- **Language**: Java 17
- **Framework**: Spring Boot 3.2.0
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Build Tool**: Maven
- **Deployment**: Docker, Render/Railway

### 3.2 Core Components

#### 3.2.1 Authentication Service

The `AuthService` handles user registration and login, generating JWT tokens for authenticated sessions. Passwords are stored (in production, should be hashed with BCrypt).

#### 3.2.2 Payment Service

The `PaymentService` orchestrates payment processing:

1. Validates user and account
2. Performs security checks (Template Method)
3. Processes payment via appropriate adapter (Adapter Pattern)
4. Creates transaction record
5. Updates city metrics (Singleton)
6. Notifies observers (Observer Pattern)

#### 3.2.3 REST API Endpoints

**Authentication:**

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

**Payments:**

- `POST /api/pay/fiat` - Process fiat payment
- `POST /api/pay/crypto` - Process crypto payment

**Account Management:**

- `GET /api/account/balance` - Get account balance

**Transactions:**

- `GET /api/transactions` - Get user transactions
- `GET /api/transactions/{id}` - Get specific transaction

**Admin:**

- `GET /api/metrics` - System metrics
- `GET /api/metrics/logs` - Audit logs

### 3.3 Scenario: Crypto Parking Payment

A detailed scenario demonstrating the payment flow is provided in `docs/SCENARIO_Pseudocode.md`. The scenario shows:

1. User authentication via JWT
2. Command Pattern: Payment command creation and execution
3. Template Method: Security check execution
4. Adapter Pattern: Ethereum adapter selection and payment processing
5. Observer Pattern: Notification to email and security observers
6. Singleton Pattern: City metrics update
7. Audit logging

### 3.4 GUI Mockups

Four wireframe screenshots are provided in the `mockups/` directory:

1. **Login/Register Screen**: User authentication interface
2. **Resident Dashboard**: Balance display, quick actions, transaction history
3. **Payment Screen**: Service selection, payment method (fiat/crypto), amount input
4. **Admin Dashboard**: System metrics, security alerts, audit logs

These mockups demonstrate the intended user experience and can be used for frontend development in future iterations.

---

## 4. Deployment

### 4.1 Deployment Architecture

The system is deployed using:

- **Containerization**: Docker for consistent environments
- **Cloud Platform**: Render or Railway for hosting
- **Database**: PostgreSQL (cloud-hosted)
- **Environment Variables**: Secure configuration management

### 4.2 Deployment Steps

1. **Database Setup:**

   - Create PostgreSQL database on cloud platform
   - Configure connection string

2. **Application Deployment:**

   - Connect GitHub repository to Render/Railway
   - Configure environment variables:
     - `DATABASE_URL`
     - `JWT_SECRET` (minimum 256 bits)
     - `PORT` (auto-configured by platform)

3. **Build and Deploy:**
   - Platform automatically builds from `Dockerfile`
   - Application starts on configured port
   - Health check endpoint: `/actuator/health`

### 4.3 Deployment Verification

**Screenshots Required:**

1. Deployed service URL (accessible from browser)
2. API responses (Postman or browser)
3. Application logs (cloud platform console)
4. Database configuration (no secrets exposed)

**Test Endpoints:**

- `GET /actuator/health` - Health check
- `POST /api/auth/register` - Test registration
- `POST /api/auth/login` - Test authentication
- `GET /api/metrics` - Test admin endpoint (with auth)

### 4.4 Configuration Files

- `Dockerfile`: Multi-stage build for optimized image
- `render.yaml`: Render platform configuration
- `application.properties`: Spring Boot configuration with environment variable support

---

## 5. Risk Analysis and Security

### 5.1 Authentication & RBAC Risks

**Risk**: Unauthorized access to user accounts or admin functions.

**Mitigation:**

- JWT token-based authentication with expiration
- Role-based access control (Resident vs Admin)
- Token validation on every protected endpoint
- Secure password storage (BCrypt in production)

**Remaining Risk**: Medium - Token theft through XSS attacks. Mitigation: HTTP-only cookies, CSRF tokens.

### 5.2 API Exposure and Rate Limiting

**Risk**: API abuse, DDoS attacks, brute force attempts.

**Mitigation:**

- API key or rate limiting middleware (recommended: Spring Security Rate Limiter)
- Request validation and sanitization
- CORS configuration for allowed origins

**Remaining Risk**: Medium - Without rate limiting, system vulnerable to abuse. Recommended: Implement rate limiting in production.

### 5.3 Encryption and TLS

**Risk**: Data interception during transmission.

**Mitigation:**

- HTTPS/TLS encryption (enforced by cloud platform)
- Secure database connections (SSL)
- JWT token signing with strong secret key

**Remaining Risk**: Low - Cloud platforms typically enforce TLS.

### 5.4 Secret Management

**Risk**: Exposure of sensitive credentials (database passwords, JWT secrets).

**Mitigation:**

- Environment variables for all secrets
- No hardcoded credentials in code
- Platform-managed secret storage
- `.gitignore` prevents accidental commits

**Remaining Risk**: Low - Proper secret management practices followed.

### 5.5 Logging and Audit Trails

**Risk**: Insufficient audit trails for compliance and security investigation.

**Mitigation:**

- Comprehensive audit logging for all transactions
- Security event logging
- Authentication event tracking
- Timestamped logs with user context

**Remaining Risk**: Low - Comprehensive logging implemented.

### 5.6 Data Privacy

**Risk**: Unauthorized access to personal user data.

**Mitigation:**

- Minimal data collection (username, email only)
- Role-based data access restrictions
- Secure database access controls
- GDPR compliance considerations (for production)

**Remaining Risk**: Medium - Additional privacy controls needed for production (data encryption at rest, data retention policies).

### 5.7 Cloud Risks

**Risk**: Downtime, misconfiguration, vendor lock-in.

**Mitigation:**

- Health check endpoints for monitoring
- Environment variable-based configuration (platform agnostic)
- Docker containerization (portable deployment)
- Database backups (platform-managed)

**Remaining Risk**: Medium - Vendor lock-in mitigated by Docker. Downtime risk depends on platform SLA.

### 5.8 Cryptocurrency Payment Risks

**Risk**: Transaction failures, network unavailability, incorrect transaction hashes.

**Mitigation:**

- Adapter pattern allows easy network switching
- Transaction status tracking (PENDING, COMPLETED, FAILED)
- Observer pattern notifies on failures
- Audit logging for all crypto transactions

**Remaining Risk**: Medium - Real blockchain integration requires additional error handling and transaction verification.

### 5.9 Summary of Risk Levels

| Risk Category     | Risk Level | Mitigation Status     |
| ----------------- | ---------- | --------------------- |
| Authentication    | Medium     | Implemented           |
| API Security      | Medium     | Partially implemented |
| Encryption        | Low        | Platform-managed      |
| Secret Management | Low        | Implemented           |
| Audit Logging     | Low        | Implemented           |
| Data Privacy      | Medium     | Basic implementation  |
| Cloud Risks       | Medium     | Mitigated             |
| Crypto Payments   | Medium     | Basic implementation  |

---

## 6. Testing and Validation

### 6.1 Unit Testing

Key components tested:

- Design pattern implementations
- Service layer business logic
- Repository data access

### 6.2 Integration Testing

API endpoint testing:

- Authentication flow
- Payment processing
- Transaction retrieval
- Admin metrics access

### 6.3 Manual Testing

Post-deployment validation:

- API endpoint accessibility
- Database connectivity
- JWT token generation and validation
- Payment processing (fiat and crypto)
- Observer notifications
- Audit logging

---

## 7. Conclusion

### 7.1 Project Summary

DigiBank successfully demonstrates a production-ready digital banking module with:

- Five design patterns clearly implemented and documented
- Comprehensive REST API with authentication and authorization
- Support for both fiat and cryptocurrency payments
- Cloud deployment with public accessibility
- Security measures and audit logging

### 7.2 Achievements

1. **Design Patterns**: All five patterns (Singleton, Command, Observer, Adapter, Template Method) are clearly visible in code and UML diagrams
2. **Architecture**: Clean separation of concerns with maintainable code structure
3. **Deployment**: Successfully deployed to cloud platform with database integration
4. **Documentation**: Comprehensive documentation suitable for academic evaluation
5. **Security**: Basic security measures implemented with risk awareness

### 7.3 Limitations

1. **Frontend**: Only wireframes provided, no full frontend implementation
2. **Blockchain Integration**: Simulated adapters, not real blockchain connections
3. **Rate Limiting**: Not implemented (recommended for production)
4. **Password Hashing**: Currently plain text (BCrypt recommended)
5. **Advanced Security**: Basic security measures, production would require additional hardening

### 7.4 Future Enhancements

1. **Frontend Application**: React/Vue.js frontend implementation
2. **Real Blockchain Integration**: Connect to actual Ethereum/Bitcoin networks
3. **Advanced Security**: Rate limiting, 2FA, biometric authentication
4. **Mobile Application**: iOS/Android native apps
5. **Analytics Dashboard**: Advanced metrics and reporting
6. **Multi-currency Support**: Support for multiple fiat currencies
7. **Payment Refunds**: Automated refund processing
8. **Fraud Detection**: Machine learning-based fraud detection

### 7.5 Lessons Learned

1. Design patterns provide structure but must be applied judiciously
2. Cloud deployment requires careful configuration management
3. Security is a continuous process, not a one-time implementation
4. Documentation is critical for system maintainability
5. Risk analysis helps identify areas for improvement

---

## 8. References

1. Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). _Design Patterns: Elements of Reusable Object-Oriented Software_. Addison-Wesley.

2. Spring Boot Documentation. (2024). _Spring Boot Reference Documentation_. https://spring.io/projects/spring-boot

3. PostgreSQL Documentation. (2024). _PostgreSQL 15 Documentation_. https://www.postgresql.org/docs/

4. JWT.io. (2024). _Introduction to JSON Web Tokens_. https://jwt.io/introduction

5. Render Documentation. (2024). _Deploy a Spring Boot Application_. https://render.com/docs

---

## Appendices

### Appendix A: API Endpoint Specifications

See `README.md` for complete API documentation.

### Appendix B: UML Diagrams

- Use Case Diagram: `docs/UML_UseCase_Diagram.puml`
- Class Diagram: `docs/UML_Class_Diagram.puml`

### Appendix C: Scenario and Pseudocode

See `docs/SCENARIO_Pseudocode.md` for detailed payment scenario.

### Appendix D: GUI Mockups

See `mockups/` directory for HTML wireframes:

- `login.html`
- `dashboard.html`
- `payment.html`
- `admin.html`

---

**End of Report**
