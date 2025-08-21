# Semantic Versioning (SemVer) in a Nutshell

Semantic Versioning is a three-part numbering system for software releases: **MAJOR.MINOR.PATCH**. It's a clear way to communicate what kind of changes are included in a new version.

## The Three Parts

* **PATCH**: Incremented for backward-compatible **bug fixes**.
* **MINOR**: Incremented for backward-compatible **new features**.
* **MAJOR**: Incremented for **breaking changes** that are not backward-compatible.

## Conventional Commits

Conventional Commits is a widely-used standard for commit messages that makes them "machine-readable." It provides the essential link for **automating** Semantic Versioning.

A commit message follows this structure: `<type>[optional scope]: <description>`

### Key Commit Types and Their Impact on Versioning

| Commit Type | Purpose | SemVer Impact |
| :--- | :--- | :--- |
| **`fix:`** | A bug fix. | **PATCH** version bump. |
| **`feat:`** | A new feature. | **MINOR** version bump. |
| **`BREAKING CHANGE:`** | A non-backward-compatible change. | **MAJOR** version bump. |

Other types like `docs:`, `test:`, or `chore:` are used for other changes and do not trigger a version bump.

## The Automated Workflow

When a tool like `semantic-release` is used, the workflow is automated and seamless:

1.  Developers write commit messages following the Conventional Commits standard.
2.  On push to the main branch, the automation tool scans the commit history.
3.  Based on the commit types, it automatically determines the correct SemVer increment (e.g., a `feat:` commit triggers a minor version bump).
4.  The tool then updates the version number, generates a changelog, creates a Git tag, and can even publish the new package.

---

### The TOML Configuration

The following `pyproject.toml` snippet configures the `semantic-release` tool for a Python project. It links the automated versioning process to your project files and CI/CD pipeline.

```toml
[tool.semantic_release]
version_variable = [
  "pyproject.toml:project.version"
]
upload_to_pypi = true
build_command = "python -m build"
changelog_file = "CHANGELOG.md"
commit_message = "chore(release): {version}"
tag_format = "v{version}"
````

### Explanation of the TOML Configuration

  * **`version_variable`**: This tells `semantic-release` where to find and update the version string in your project. In this case, it targets the `project.version` key within the `pyproject.toml` file itself.
  * **`upload_to_pypi`**: When set to `true`, the tool will automatically publish the new version to the Python Package Index (PyPI) after a successful release.
  * **`build_command`**: This specifies the command used to build the distributable package files (e.g., `.tar.gz`, `.whl`). The tool runs this command before attempting to upload the package.
  * **`changelog_file`**: This is the path to the Markdown file where the tool will automatically generate a summary of changes for each release, based on the commit messages.
  * **`commit_message`**: This is a template for the commit message that `semantic-release` will use to create a new commit for the version bump. The `{version}` placeholder will be replaced with the new version number.
  * **`tag_format`**: This defines the format for the Git tag that will be created for each release (e.g., `v1.2.3`). This allows for consistent and machine-readable tags in your repository's history.
