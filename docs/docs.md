# Documentation

The tool used in generating documentation is `mkdocs`.

## Using `generate_ref_docs.py`

This script is designed to generate API reference documentation for a Python package. Here’s a brief overview of how to use it:

### Setup

   Ensure that you have the required tools installed and that you are in the correct virtual environment.

   ```bash
   poetry install
   ```

### Run the Script

Execute the script with poetry to generate the documentation. The script takes several command-line arguments:

```bash
poetry run scripts.generate_ref_docs:main
```

`--output-dir`: Specifies the directory where the generated documentation will be saved. The default is docs/reference.

`--package-name`: The name of the package for which documentation is being generated. If not provided, it is inferred from the project configuration.

`--force`: If specified, the script will overwrite existing .md files in the output directory.

Example command:

```bash
poetry run scripts.generate_ref_docs:main --package-name my_package --output-dir docs/reference --force
```
This command generates the API documentation for `my_package`, saves it to the `docs/reference` directory, and overwrites existing files if they are present.

## Using MkDocs
MkDocs is a static site generator that is used to build project documentation.

Here’s how to use it:

### Building the Static Site:

To build the static site from your documentation source files, use the `mkdocs build` command:

```bash
mkdocs build
```

This command generates a static site in the site directory (by default). It compiles Markdown files and other assets into a directory that can be served by a web server.

Documentation: [MkDocs Build Documentation](https://www.mkdocs.org/getting-started/#building-the-site)

### Serving the Documentation:

For fast debugging and local development, use the mkdocs serve command:

```bash
mkdocs serve
```

This command starts a local development server, typically available at http://127.0.0.1:8000. It watches for changes to your documentation files and automatically reloads the server to reflect those changes.

Documentation: [MkDocs Serve Documentation](https://www.mkdocs.org/getting-started/#creating-a-new-project)
