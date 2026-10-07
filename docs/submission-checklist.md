# Submission Checklist - DigiBank Project

**Student:** KHUDOYOR FAKHRITDINOV  
**Student ID:** 2420003035  
**University:** Beykent University  
**Project:** DigiBank (Smart City Digital Banking Module)

## Pre-Submission Verification

Use this checklist to ensure all deliverables are complete before final submission.

---

## 📋 Deliverables Checklist

### 1. PDF Report
- [ ] Convert `docs/IEEE_Project_Report.md` to PDF
- [ ] Filename: `2420003035_KHUDOYOR_FAKHRITDINOV.pdf`
- [ ] Verify all sections are included
- [ ] Check formatting and page numbers
- [ ] Include all UML diagrams (as images)
- [ ] Include screenshots where referenced

**Command to generate PDF** (if using Pandoc):
```bash
pandoc docs/IEEE_Project_Report.md -o 2420003035_KHUDOYOR_FAKHRITDINOV.pdf --pdf-engine=xelatex
```

**Alternative**: Use online Markdown to PDF converter or Word export.

---

### 2. ZIP Archive
- [ ] Create ZIP file: `2420003035_KHUDOYOR_FAKHRITDINOV.zip`
- [ ] Verify ZIP size ≤ 5MB
- [ ] Include all source code (`src/` directory)
- [ ] Include frontend (`frontend/` directory)
- [ ] Include documentation (`docs/` directory)
- [ ] Include UML diagrams (PNG format in `docs/uml/`)
- [ ] Include screenshots (`docs/screenshots/`)
- [ ] Include configuration files:
  - [ ] `pom.xml`
  - [ ] `Dockerfile`
  - [ ] `render.yaml`
  - [ ] `application.properties`
- [ ] Include `README.md`
- [ ] **Exclude**:
  - [ ] `target/` directory (build artifacts)
  - [ ] `.git/` directory
  - [ ] `node_modules/` (if any)
  - [ ] IDE-specific files (`.idea/`, `.vscode/`)

**ZIP Creation Command**:
```bash
# Windows PowerShell
Compress-Archive -Path src,frontend,docs,pom.xml,Dockerfile,render.yaml,README.md -DestinationPath 2420003035_KHUDOYOR_FAKHRITDINOV.zip

# Linux/Mac
zip -r 2420003035_KHUDOYOR_FAKHRITDINOV.zip src/ frontend/ docs/ pom.xml Dockerfile render.yaml README.md -x "*/target/*" "*/node_modules/*" "*/.git/*"
```

---

### 3. Source Code
- [ ] All Java source files present (`src/main/java/com/digibank/`)
- [ ] All design patterns implemented:
  - [ ] Singleton (`pattern/singleton/CityController.java`)
  - [ ] Command (`pattern/command/*.java`)
  - [ ] Observer (`pattern/observer/*.java`)
  - [ ] Adapter (`pattern/adapter/*.java`)
  - [ ] Template Method (`pattern/template/*.java`)
- [ ] All controllers present
- [ ] All services present
- [ ] All models/entities present
- [ ] All repositories present
- [ ] Configuration files present

---

### 4. UML Diagrams
- [ ] Use Case Diagram: `docs/UML_UseCase_Diagram.puml` ✅
- [ ] Class Diagram: `docs/UML_Class_Diagram.puml` ✅
- [ ] Sequence Diagram: `docs/uml/UML_Sequence_Diagram.puml` ✅
- [ ] Deployment Diagram: `docs/uml/UML_Deployment_Diagram.puml` ✅
- [ ] **Export all to PNG**:
  - [ ] `docs/uml/UML_UseCase_Diagram.png`
  - [ ] `docs/uml/UML_Class_Diagram.png`
  - [ ] `docs/uml/UML_Sequence_Diagram.png`
  - [ ] `docs/uml/UML_Deployment_Diagram.png`

**Export Instructions**: See `docs/uml/README.md`

---

### 5. Frontend
- [ ] All frontend files present (`frontend/` directory)
- [ ] `index.html` present
- [ ] All page components present:
  - [ ] `src/pages/Login.js`
  - [ ] `src/pages/Dashboard.js`
  - [ ] `src/pages/Payments.js`
  - [ ] `src/pages/Monitoring.js`
  - [ ] `src/pages/Alerts.js`
- [ ] Styles present (`src/styles/main.css`)
- [ ] Utilities present (`src/utils/*.js`)
- [ ] Frontend README present

---

### 6. Screenshots
- [ ] Login page screenshot
- [ ] Dashboard screenshot
- [ ] Payment forms screenshot
- [ ] Monitoring page screenshot (Admin)
- [ ] Alerts page screenshot
- [ ] API test screenshots (Postman/curl)
- [ ] Health check screenshot
- [ ] Deployment screenshot (Render dashboard)

**Location**: `docs/screenshots/`

---

### 7. Documentation
- [ ] `README.md` (main project README)
- [ ] `docs/requirements-mapping.md` ✅
- [ ] `docs/tests.md` ✅
- [ ] `docs/risk-analysis.md` ✅
- [ ] `docs/submission-checklist.md` (this file) ✅
- [ ] `docs/IEEE_Project_Report.md`
- [ ] `frontend/README.md` ✅
- [ ] `docs/uml/README.md` ✅

---

## 🔧 Build & Deployment Verification

### Backend Build
- [ ] Maven build succeeds: `mvn clean package`
- [ ] JAR file generated: `target/digibank-1.0.0.jar`
- [ ] No compilation errors
- [ ] All tests pass (if any)

**Build Command**:
```bash
mvn clean package -DskipTests
```

### Docker Build
- [ ] Docker image builds successfully
- [ ] Dockerfile is correct (Java 17 base image)
- [ ] Multi-stage build works

**Docker Commands**:
```bash
# Build image
docker build -t digibank:latest .

# Run container (local test)
docker run -p 8080:8080 \
  -e DATABASE_URL=jdbc:postgresql://localhost:5432/digibank \
  -e DB_USERNAME=postgres \
  -e DB_PASSWORD=postgres \
  -e JWT_SECRET=your-secret-key \
  digibank:latest
```

### Render Deployment
- [ ] Service is deployed and running
- [ ] Health check returns UP: `GET /actuator/health`
- [ ] Database connection working
- [ ] Environment variables configured:
  - [ ] `DATABASE_URL` or `JDBC_DATABASE_URL`
  - [ ] `DB_USERNAME`
  - [ ] `DB_PASSWORD`
  - [ ] `JWT_SECRET`
  - [ ] `PORT`

**Render URLs** (Document these):
- Backend API: `https://your-app.onrender.com`
- Health Check: `https://your-app.onrender.com/actuator/health`

**Verification Commands**:
```bash
# Health check
curl https://your-app.onrender.com/actuator/health

# Test login
curl -X POST https://your-app.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'
```

---

## ✅ Functional Verification

### API Endpoints
- [ ] `POST /api/auth/register` - Working
- [ ] `POST /api/auth/login` - Working
- [ ] `GET /api/account/balance` - Working (with auth)
- [ ] `POST /api/pay/fiat` - Working (with auth)
- [ ] `POST /api/pay/crypto` - Working (with auth)
- [ ] `GET /api/transactions` - Working (with auth)
- [ ] `GET /api/metrics` - Working (Admin only)
- [ ] `GET /api/metrics/logs` - Working (Admin only)
- [ ] `GET /actuator/health` - Working

### Frontend Pages
- [ ] Login page loads and works
- [ ] Registration works
- [ ] Dashboard loads and displays data
- [ ] Payment forms submit successfully
- [ ] Monitoring page accessible (Admin)
- [ ] Alerts page displays notifications
- [ ] Navigation works correctly
- [ ] Logout works

### Design Patterns
- [ ] Singleton pattern verified (CityController)
- [ ] Command pattern verified (PaymentCommand)
- [ ] Observer pattern verified (Notifications)
- [ ] Adapter pattern verified (Crypto adapters)
- [ ] Template Method verified (Security checks)

---

## 📝 File Naming Conventions

### Required Format
- **PDF Report**: `2420003035_KHUDOYOR_FAKHRITDINOV.pdf`
- **ZIP Archive**: `2420003035_KHUDOYOR_FAKHRITDINOV.zip`

### Verification
- [ ] Student ID matches: `2420003035`
- [ ] Name matches: `KHUDOYOR_FAKHRITDINOV`
- [ ] No spaces in filenames
- [ ] All uppercase for name

---

## 🔍 Final Checks

### Code Quality
- [ ] No hardcoded secrets
- [ ] No Lombok usage (explicit getters/setters)
- [ ] Explicit loggers (LoggerFactory.getLogger)
- [ ] Proper error handling
- [ ] Code comments where needed

### Documentation Quality
- [ ] All sections complete
- [ ] No placeholder text remaining
- [ ] URLs updated (replace `your-render-app.onrender.com`)
- [ ] Screenshots referenced correctly
- [ ] Grammar and spelling checked

### Deployment
- [ ] Backend accessible
- [ ] Database connected
- [ ] Health check working
- [ ] CORS configured correctly
- [ ] Environment variables set

---

## 📊 Submission Summary

Before final submission, verify:

1. **PDF Report**: ✅ Generated and named correctly
2. **ZIP Archive**: ✅ Created, ≤5MB, contains all required files
3. **Source Code**: ✅ Complete and functional
4. **UML Diagrams**: ✅ All 4 diagrams exported to PNG
5. **Frontend**: ✅ Complete and functional
6. **Screenshots**: ✅ All required screenshots captured
7. **Documentation**: ✅ All documents complete
8. **Deployment**: ✅ Backend deployed and accessible
9. **Testing**: ✅ All critical tests passed
10. **File Naming**: ✅ Correct format

---

## 🚀 Final Steps

1. **Generate PDF Report**
   ```bash
   # Use Pandoc, Word, or online converter
   # Save as: 2420003035_KHUDOYOR_FAKHRITDINOV.pdf
   ```

2. **Export UML Diagrams to PNG**
   - Use PlantUML online server or VS Code extension
   - Save to `docs/uml/` directory

3. **Capture Screenshots**
   - Frontend pages
   - API responses
   - Deployment status
   - Save to `docs/screenshots/`

4. **Create ZIP Archive**
   ```bash
   # Verify size ≤ 5MB
   # Include all required files
   # Exclude build artifacts
   ```

5. **Final Verification**
   - Test ZIP can be extracted
   - Verify all files present
   - Check file sizes
   - Test backend is accessible

6. **Submit**
   - Upload PDF report
   - Upload ZIP archive
   - Verify submission successful

---

## 📞 Support Notes

- **Render URL**: Document your actual Render deployment URL
- **Database**: Document connection details (for reference only)
- **Issues**: Document any known limitations or issues

---

**Checklist Status**: ⚠️ **Complete Before Submission**

**Last Updated**: [Current Date]  
**Next Action**: Generate PDF and create ZIP archive

