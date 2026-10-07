# UML Diagrams - DigiBank Project

This directory contains PlantUML source files for all system diagrams. All diagrams are verified to match the codebase exactly with no placeholders.

## Available Diagrams

1. **Use Case Diagram**: `../UML_UseCase_Diagram.puml`
   - Shows actors (Resident, Admin) and their use cases
   - Includes relationships between use cases
   - Verified: All use cases match implemented functionality

2. **Class Diagram**: `../UML_Class_Diagram.puml`
   - Complete class structure with all relationships
   - All design patterns clearly marked
   - All services, controllers, models, and repositories included
   - Verified: Matches codebase exactly (no placeholders)

3. **Sequence Diagram**: `UML_Sequence_Diagram.puml`
   - Shows complete login and crypto payment flow
   - Includes all design patterns in action
   - Shows FraudRiskAnalysisService integration
   - Verified: Sequence matches actual code execution

4. **Deployment Diagram**: `UML_Deployment_Diagram.puml`
   - Shows Render cloud architecture
   - Client → Frontend → Backend → Database flow
   - Includes external services (Crypto Networks)
   - Verified: Matches deployment configuration

## Design Patterns in Diagrams

All design patterns are clearly marked in the Class Diagram:

- **Singleton**: `CityController` - Central system controller
- **Command**: `PaymentCommand`, `FiatPaymentCommand`, `CryptoPaymentCommand` - Payment execution encapsulation
- **Observer**: `NotificationObserver`, `NotificationSubject` - Event notifications
- **Adapter**: `CryptoPaymentAdapter`, `EthereumAdapter`, `BitcoinAdapter`, `PolygonAdapter` - Multi-blockchain integration
- **Template Method**: `SecurityCheckTemplate`, `PaymentSecurityCheck` - Standardized security checks

## Export Instructions

### Method 1: Online PlantUML Server (Recommended)

1. Visit http://www.plantuml.com/plantuml/uml/
2. Open each `.puml` file in a text editor
3. Copy the entire contents
4. Paste into the PlantUML online editor
5. Click "Submit" to render
6. Right-click the rendered diagram → "Save image as..." → Save as PNG
7. Save to `docs/uml/` directory with naming: `UML_UseCase_Diagram.png`, etc.

### Method 2: VS Code Extension

1. Install "PlantUML" extension in VS Code
2. Open the `.puml` file
3. Press `Alt+D` (or right-click → "Preview PlantUML")
4. Right-click the preview → "Export Current Diagram" → PNG
5. Save to `docs/uml/` directory

### Method 3: Command Line (Java Required)

```bash
# Download PlantUML JAR
wget http://sourceforge.net/projects/plantuml/files/plantuml.jar/download -O plantuml.jar

# Export all diagrams
java -jar plantuml.jar -tpng docs/UML_UseCase_Diagram.puml -o docs/uml/
java -jar plantuml.jar -tpng docs/UML_Class_Diagram.puml -o docs/uml/
java -jar plantuml.jar -tpng docs/uml/UML_Sequence_Diagram.puml -o docs/uml/
java -jar plantuml.jar -tpng docs/uml/UML_Deployment_Diagram.puml -o docs/uml/
```

### Method 4: Docker (If Available)

```bash
docker run -v "$(pwd):/work" plantuml/plantuml -tpng /work/docs/UML_UseCase_Diagram.puml -o /work/docs/uml/
docker run -v "$(pwd):/work" plantuml/plantuml -tpng /work/docs/UML_Class_Diagram.puml -o /work/docs/uml/
docker run -v "$(pwd):/work" plantuml/plantuml -tpng /work/docs/uml/*.puml
```

## Expected Output Files

After export, you should have:
- `docs/uml/UML_UseCase_Diagram.png`
- `docs/uml/UML_Class_Diagram.png`
- `docs/uml/UML_Sequence_Diagram.png`
- `docs/uml/UML_Deployment_Diagram.png`

## Quality Settings

For report inclusion, ensure:
- **Resolution**: At least 300 DPI
- **Format**: PNG (preferred) or SVG
- **Size**: Large enough to be readable when printed
- **Background**: White or transparent

## Diagram Verification

All diagrams have been verified to:
- ✅ Match the codebase exactly
- ✅ Have no placeholders or TODO comments
- ✅ Include all relevant classes and relationships
- ✅ Show correct sequence flows
- ✅ Mark design patterns clearly
- ✅ Use proper UML notation

## Troubleshooting

- **Diagrams not rendering**: Check PlantUML syntax, ensure all packages are properly closed
- **Low quality**: Use SVG format and convert to PNG at high DPI
- **Missing elements**: All diagrams have been verified to match the codebase exactly

## Notes

- All diagrams use standard PlantUML syntax
- Diagrams are designed for Smart City banking context
- Design patterns are clearly marked in Class Diagram
- Sequence Diagram shows complete login + payment flow with all services
- Deployment Diagram reflects Render cloud architecture
- All relationships and flows match actual code implementation
