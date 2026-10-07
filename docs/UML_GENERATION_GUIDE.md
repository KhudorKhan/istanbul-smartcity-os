# UML Diagram Generation Guide

## Overview
The UML diagrams are provided in PlantUML format (`.puml` files). This guide explains how to generate visual diagrams from these files.

## Files
- `UML_UseCase_Diagram.puml` - Use Case Diagram
- `UML_Class_Diagram.puml` - Class Diagram

## Method 1: Online PlantUML Server (Easiest)

1. Visit: http://www.plantuml.com/plantuml/uml/
2. Copy the contents of a `.puml` file
3. Paste into the online editor
4. The diagram will render automatically
5. Right-click and "Save image as..." to download PNG/SVG

## Method 2: VS Code Extension

1. Install "PlantUML" extension in VS Code
2. Open the `.puml` file
3. Press `Alt+D` (or right-click → "Preview PlantUML")
4. Export as PNG/SVG

## Method 3: Command Line (Java Required)

1. Download PlantUML JAR: http://plantuml.com/download
2. Run command:
   ```bash
   java -jar plantuml.jar docs/UML_UseCase_Diagram.puml
   java -jar plantuml.jar docs/UML_Class_Diagram.puml
   ```
3. PNG files will be generated in the same directory

## Method 4: Docker

```bash
docker run -d -p 8080:8080 plantuml/plantuml-server:jetty
# Then access http://localhost:8080
```

## Recommended for Submission

For academic submission, generate PNG or PDF versions:
- Use Method 1 (online) for quick generation
- Save as high-resolution PNG
- Include in report or as separate files

## Diagram Descriptions

### Use Case Diagram
Shows actors (Resident, Admin, etc.) and their interactions with the system use cases.

### Class Diagram
Shows the complete class structure, relationships, and design pattern implementations.

Both diagrams clearly mark where each design pattern is applied.


