# AbarORM Documentation

Welcome to the documentation for the AbarORM project. This guide will help you get started with setting up, building, and deploying your documentation using MkDocs.

## Installation

**Install MkDocs and MkDocs Material Theme**

   You can install `MkDocs` and the `mkdocs-material` theme using pip. Open your terminal or command prompt and run the following command:
   ```bash
   pip install -r requirements.txt
   ```
## Building Your Documentation
- **Serve Locally**
To preview your documentation locally, run:
```bash
mkdocs serve
```
This command will start a local server. Open your web browser and go to `http://127.0.0.1:8000` to view your documentation. The server will automatically reload when you make changes to your files.

- **Build for Production**
When you are ready to build the static files for production, run:
```bash
mkdocs build
```
This command generates a `site` directory containing the static files of your documentation.

