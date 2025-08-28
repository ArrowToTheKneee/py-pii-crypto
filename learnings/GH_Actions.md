# GitHub Actions Cheat Sheet

This cheat sheet provides an overview of GitHub Actions concepts, common YAML syntax, and useful examples for CI/CD pipelines.

---

## 1. Key Concepts

* **Workflow**: A configurable automated process made up of **jobs**. Stored in `.github/workflows/*.yml`
* **Job**: A set of steps executed on the same runner.
* **Step**: A single task, can be a script or an action.
* **Action**: Reusable code you can call in a workflow (e.g., `actions/checkout`).
* **Runner**: Machine that executes your workflow (GitHub-hosted or self-hosted).
* **Event**: Triggers a workflow (push, pull\_request, schedule, workflow\_dispatch, etc.)
* **Artifact**: File or directory uploaded from a workflow for later download.

---

## 2. Workflow YAML Structure

```yaml
name: CI Pipeline             # Optional workflow name

on:
  push:
    branches: [main]           # Trigger workflow on push to main
  pull_request:
    branches: [main]           # Trigger workflow on PR to main

jobs:
    <Job Name>:                # Optional descriptive name
    runs-on: ubuntu-latest     # Runner type
    needs: <other_job_id>      # Optional: make this job depend on another job
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest --junitxml=reports/results.xml

      - name: Upload test reports
        uses: actions/upload-artifact@v4
        with:
          name: pytest-report
          path: reports/
```

---

## 3. Common `on:` Events

* `push` → triggers on push to repo
* `pull_request` → triggers when a PR is created, updated, or merged
* `workflow_dispatch` → manually trigger workflow via GitHub UI
* `schedule` → cron jobs
* `release` → triggers when a release is created

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch: {}
```

---

## 4. Steps

### Running commands

```yaml
- name: Run shell commands
  run: |
    echo "Hello World"
    pytest
```

### Using actions

```yaml
- name: Checkout repository
  uses: actions/checkout@v4

- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

### Conditional execution

```yaml
- name: Run only on main branch
  if: github.ref == 'refs/heads/main'
  run: echo "This runs only on main branch"
```

---

## 5. Jobs

* Run sequentially using `needs:`
* Run in parallel by default
* Example:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build job"

  test:
    runs-on: ubuntu-latest
    needs: build   # waits for build to complete
    steps:
      - run: echo "Test job"
```

---

## 6. Artifacts

* Upload test results or reports

```yaml
- name: Upload pytest HTML report
  uses: actions/upload-artifact@v4
  with:
    name: pytest-html
    path: reports/pytest-report.html
```

* Download artifacts in another workflow or job using `actions/download-artifact`.

---

## 7. GitHub Pages Deployment

* Use `peaceiris/actions-gh-pages@v4`
* Example:

```yaml
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./reports
    publish_branch: gh-pages
```

* Ensure GitHub Pages is configured in repo settings with `gh-pages` branch.

---

## 8. CI/CD Best Practices

* **Separate workflows**: `ci.yml` for tests, `release.yml` for release automation
* **Use matrix builds** to test multiple Python versions or OS
* **Upload artifacts** for debugging failed jobs
* **Fail PR merges if CI fails** by enabling branch protection rules
* **Keep reports out of main branch** unless needed; use artifacts or gh-pages
* **Linting & formatting**: integrate `black` or `ruff`
* **Semantic versioning**: integrate `python-semantic-release` for automated releases

---

## 9. Example Full CI Workflow with pytest, coverage, linting, and gh-pages deployment

```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .[dev]

      - name: Lint with ruff
        run: ruff check .

      - name: Format check with black
        run: black --check .

      - name: Run tests with coverage and HTML report
        run: |
          mkdir -p reports
          pytest tests --cov=src --cov-report=xml:reports/coverage.xml --html=reports/pytest-report.html --self-contained-html

      - name: Upload pytest & coverage reports
        uses: actions/upload-artifact@v4
        with:
          name: pytest-artifacts
          path: |
            reports/coverage.xml
            reports/pytest-report.html

      - name: Deploy HTML report to gh-pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./reports
          publish_branch: gh-pages
```
