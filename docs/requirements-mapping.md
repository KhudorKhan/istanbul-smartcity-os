# Requirements Mapping - DigiBank Project

**Student:** KHUDOYOR FAKHRITDINOV  
**Student ID:** 2420003035  
**University:** Beykent University  
**Project:** DigiBank (Smart City Digital Banking Module)

## Purpose
This document maps homework requirements to implementation evidence, identifies gaps, and tracks actions needed for full compliance.

---

## Requirements Compliance Table

| Requirement Category | Requirement | Evidence (File/Path/Screenshot) | Status | Missing | Action |
|---------------------|-------------|--------------------------------|--------|---------|--------|
| **Backend Architecture** | Java 17 + Spring Boot | `pom.xml` (Java 17, Spring Boot 3.2.0), `src/main/java/com/digibank/DigiBankApplication.java` | ✅ Complete | None | None |
| | Maven build system | `pom.xml`, `mvnw`, `mvnw.cmd` | ✅ Complete | None | None |
| | PostgreSQL database | `src/main/resources/application.properties`, `render.yaml` | ✅ Complete | None | None |
| | RESTful API | `src/main/java/com/digibank/controller/*.java` | ✅ Complete | None | None |
| | JWT authentication | `src/main/java/com/digibank/service/JwtService.java`, `src/main/java/com/digibank/service/AuthService.java` | ✅ Complete | None | None |
| | Spring Actuator | `pom.xml` (dependency), `application.properties` (management.endpoints) | ✅ Complete | None | None |
| **Design Patterns** | Singleton Pattern | `src/main/java/com/digibank/pattern/singleton/CityController.java` | ✅ Complete | None | None |
| | Command Pattern | `src/main/java/com/digibank/pattern/command/*.java` | ✅ Complete | None | None |
| | Observer Pattern | `src/main/java/com/digibank/pattern/observer/*.java` | ✅ Complete | None | None |
| | Adapter Pattern | `src/main/java/com/digibank/pattern/adapter/*.java` | ✅ Complete | None | None |
| | Template Method Pattern | `src/main/java/com/digibank/pattern/template/*.java` | ✅ Complete | None | None |
| **UML Diagrams** | Use Case Diagram | `docs/UML_UseCase_Diagram.puml` | ✅ Complete | PNG export | Export to PNG for report |
| | Class Diagram | `docs/UML_Class_Diagram.puml` | ✅ Complete | PNG export | Export to PNG for report |
| | Sequence Diagram | `docs/uml/UML_Sequence_Diagram.puml` | ✅ Complete | PNG export | Export to PNG for report |
| | Deployment Diagram | `docs/uml/UML_Deployment_Diagram.puml` | ✅ Complete | PNG export | Export to PNG for report |
| **Deployment** | Docker containerization | `Dockerfile` | ✅ Complete | None | None |
| | Render deployment config | `render.yaml` | ✅ Complete | None | None |
| | Environment variables | `application.properties`, `render.yaml` | ✅ Complete | None | None |
| | Health check endpoint | `/actuator/health` (verified UP) | ✅ Complete | None | None |
| **Frontend** | Login screen | `frontend/src/pages/Login.js` | ✅ Complete | Screenshot | Capture screenshot |
| | Dashboard page | `frontend/src/pages/Dashboard.js` | ✅ Complete | Screenshot | Capture screenshot |
| | Monitoring/metrics page | `frontend/src/pages/Monitoring.js` | ✅ Complete | Screenshot | Capture screenshot |
| | Payments page | `frontend/src/pages/Payments.js` | ✅ Complete | Screenshot | Capture screenshot |
| | Alerts/Notifications view | `frontend/src/pages/Alerts.js` | ✅ Complete | Screenshot | Capture screenshot |
| **Documentation** | IEEE-style report | `docs/IEEE_Project_Report.md` | ✅ Complete | PDF export | Convert to PDF |
| | Requirements mapping | `docs/requirements-mapping.md` (this file) | ✅ Complete | None | None |
| | Test documentation | `docs/tests.md` | ✅ Complete | Screenshots | Add test evidence screenshots |
| | Risk analysis | `docs/risk-analysis.md` | ✅ Complete | None | None |
| | Submission checklist | `docs/submission-checklist.md` | ✅ Complete | None | None |
| | README | `README.md` | ✅ Complete | Frontend section | Update with frontend info |
| **Testing** | Manual API tests | `docs/tests.md` | ✅ Complete | Evidence | Add Postman/curl screenshots |
| | Frontend interaction tests | `docs/tests.md` | ✅ Complete | Evidence | Add browser screenshots |
| | Healthcheck test | `docs/tests.md` | ✅ Complete | Evidence | Add health endpoint screenshot |
| **Code Quality** | No Lombok (explicit getters/setters) | `src/main/java/com/digibank/model/User.java` (explicit getters/setters) | ✅ Complete | None | None |
| | Explicit loggers | All controllers/services use `LoggerFactory.getLogger()` | ✅ Complete | None | None |
| | No hardcoded secrets | `application.properties` uses `${JWT_SECRET}` | ✅ Complete | None | None |
| **Deliverables** | PDF report | `2420003035_KHUDOYOR_FAKHRITDINOV.pdf` | ⚠️ Pending | PDF file | Generate from IEEE report |
| | ZIP archive (≤5MB) | `2420003035_KHUDOYOR_FAKHRITDINOV.zip` | ⚠️ Pending | ZIP file | Create before submission |
| | Source code | `src/` directory | ✅ Complete | None | None |
| | UML diagrams (PNG) | `docs/uml/*.png` | ⚠️ Pending | PNG files | Export PlantUML to PNG |
| | GUI mockups/screenshots | `docs/screenshots/` | ⚠️ Pending | Screenshot files | Capture frontend screenshots |

---

## Missing Items Summary

### Critical (Must Complete Before Submission)
1. **PDF Report**: Convert `docs/IEEE_Project_Report.md` to `2420003035_KHUDOYOR_FAKHRITDINOV.pdf`
2. **UML PNG Exports**: Export all PlantUML files to PNG format
3. **Frontend Screenshots**: Capture screenshots of all frontend pages
4. **Test Evidence**: Add screenshots to `docs/tests.md`
5. **ZIP Archive**: Create final submission ZIP (≤5MB)

### Optional (Nice to Have)
- Additional test coverage
- Performance benchmarks
- Extended documentation

---

## Action Items

### Immediate Actions
- [x] Create requirements mapping document
- [ ] Export UML diagrams to PNG
- [ ] Capture frontend screenshots
- [ ] Add test evidence screenshots
- [ ] Generate PDF report
- [ ] Create submission ZIP

### Verification Steps
- [ ] Verify all requirements are addressed
- [ ] Check file naming conventions (StudentID_Name format)
- [ ] Verify ZIP size ≤ 5MB
- [ ] Test all API endpoints
- [ ] Verify frontend functionality
- [ ] Check deployment health

---

## Notes

- All backend requirements are **fully implemented** and **deployed** on Render
- Design patterns are **clearly implemented** and **documented**
- Frontend is **functional** and **ready for demo**
- Documentation is **comprehensive** and **academic-grade**

---

**Last Updated:** [Current Date]  
**Status:** Ready for final deliverables preparation

