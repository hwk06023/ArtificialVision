# Contribution Guide (Not yet ❗️)

Thank you for considering contributing to our project! We appreciate your time and effort in making our project better.


## Table of Contents
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Conclusion](#conclusion)

## Getting Started
### Prerequisites
- Git
- Python (version specified in `requirements.txt`)
- Virtual environment tool (e.g., `venv`, `conda`)

### Setting Up Locally
1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/ArtificialVision.git
   cd ArtificialVision
    ```

2. **Create a Virtual Environment**

    for venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

    for conda:
    ```bash
    conda create --name artificialvision python=3.x
    conda activate artificialvision
    ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

<br/>

## Contributing
### Creating Issues
* Use GitHub Issues to report bugs, request features, or ask questions. <br/>
* Before creating a new issue, please search existing issues to avoid duplicates. <br/>
* Clearly describe the issue, including steps to reproduce if applicable. <br/> 

### Making Changes
Making Changes
1. Create a new branch for your changes:
    ```bash
    git checkout -b feature/your_feature_name
    ```

2. Make and commit your changes. Keep your commits small and focused; they should relate to the issue you're addressing.

3. Write meaningful commit messages that provide context for your changes.
 <br/>

### Submitting Pull Requests
1. Push your branch to GitHub:
    ```
    git push origin feature/your_feature_name
    ```

2. Go to the repository on GitHub and click "Pull request" for your branch.

3. Provide a clear title and description for your pull request. Link any relevant issues.

4. Ensure your changes do not break the existing functionality. Add tests if applicable.

## Code Style
Honestsly, we don't have a strict code style guide. But we encourage you to follow the **PEP 8 style guide** for Python code.

## Testing
Explain how to run the automated tests for this system. Provide code examples and explanations for running the tests.

## Documentation
Update the [ForOfficialDocs.md](ForOfficialDocs.md) with any changes in setup, usage, or dependencies.

## Issue Reporting
Explain how to report issues or bugs in the project. Clearly describe the issue, providing the steps to reproduce and the expected outcome. Include error messages, stack traces, and system information (OS, Python version ..).

## Conclusion
Thank contributors for their interest in the project and their contributions.

