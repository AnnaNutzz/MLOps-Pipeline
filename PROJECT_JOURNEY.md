# Project Journey: Debugging the End-to-End MLOps Pipeline

This document outlines the series of real-world challenges encountered and resolved during the construction of this CI/CD pipeline. The process demonstrates a systematic approach to debugging complex integrations between version control, CI/CD servers, containerization, and application code.

### 1. Initial Jenkins Configuration
- **Problem:** The first pipeline run failed because Jenkins, by default, blocks checking out code from a local file path for security reasons.
- **Solution:** Pushed the project to a remote GitHub repository and reconfigured the Jenkins job to use the new repository URL. This is the standard, secure practice for CI/CD.

### 2. Git & GitHub Integration
- **Problem:** The initial `git push` failed because the remote repository contained a `README.md` file that didn't exist locally, causing a history conflict.
- **Solution:** Merged the remote changes with the local repository using `git pull --allow-unrelated-histories` before successfully pushing the code.

- **Problem:** A `jenkins.msi` installer (95MB) was committed to the repository, triggering a warning from GitHub about large file sizes and slowing down Git operations.
- **Solution:** Removed the large file from the Git history using `git rm --cached` and added a rule to the `.gitignore` file to prevent similar files from being committed in the future.

### 3. Jenkins Authentication & Authorization
- **Problem:** Jenkins failed to clone the repository with an `Authentication failed` error because GitHub has deprecated password-based authentication for Git operations.
- **Solution:** Generated a Personal Access Token (PAT) on GitHub with `repo` scopes and configured it as a "Username with password" credential in Jenkins.

- **Problem:** After fixing authentication, the pipeline failed with a `403 Forbidden` error.
- **Solution:** Diagnosed that the GitHub PAT, while valid, was missing the correct permissions (`repo` scope) to access the repository. The permissions were updated on GitHub, resolving the issue.

### 4. Jenkins Pipeline & Environment Setup
- **Problem:** The pipeline failed because it was configured to look for a `master` branch, but the repository's default branch was named `main`.
- **Solution:** Updated the "Branch Specifier" in the Jenkins job configuration to `*/main`.

- **Problem:** On the Windows agent, the pipeline could not find the `py` or `python` commands, as Python was not in the system's `PATH` for the Jenkins user.
- **Solution:** As a workaround for not having admin access to configure Jenkins tools globally, the `Jenkinsfile` was updated to use a hardcoded, absolute path to the Python executable.

- **Problem:** The `pip install` command failed because `numpy` required a C/C++ compiler to build from source on the agent machine, which was not available.
- **Solution:** Re-architected the pipeline to be Docker-centric. This involved building a Docker image with all dependencies pre-installed, ensuring a consistent and self-contained build environment.

### 5. Dockerfile & Build Context
- **Problem:** The `docker build` process failed because it could not find the `tests` and `data` directories.
- **Solution:** Inspected the `.dockerignore` file and found rules that were incorrectly excluding these essential directories. Removing these rules allowed Docker to correctly copy all necessary files into the image.

### 6. Cross-Platform Scripting
- **Problem:** The pipeline failed because `sh` (a Linux command) was used in the `Jenkinsfile`, but the agent was running on Windows.
- **Solution:** Replaced all `sh` steps with `bat` to ensure the commands were executed by the native Windows Batch interpreter.

- **Problem:** The deploy stage failed when trying to stop a non-existent container. The Linux error-suppression trick (`|| true`) was not compatible with Windows.
- **Solution:** Replaced `|| true` with the Windows-compatible equivalent, `|| ver > nul`, to gracefully handle the expected error.

### 7. Application & Test Execution
- **Problem:** The `pytest` stage failed inside the Docker container with a `ModuleNotFoundError` because Python did not know where to find the `app` source code.
- **Solution:** Added the `--env PYTHONPATH=/app` flag to the `docker run` command in the `Jenkinsfile`, which correctly configured the Python import path inside the container.

- **Problem:** With the import path fixed, the test suite ran but revealed a bug: one test failed with a `500 Internal Server Error`.
- **Solution:** The failing test indicated that the API crashed when receiving an empty data list. A check was added to the `/predict` endpoint in `app/main.py` to handle this case gracefully.

- **Problem:** The final `docker run` command failed because port `8080` was already in use on the host machine.
- **Solution:** Changed the port mapping in the `Jenkinsfile` to an unused port (`8088`), resolving the conflict and allowing the application to deploy successfully. 