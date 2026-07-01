# Developer Setup Guide (ELUSoC_2026)

## Environment Preparation
To set up AgentWatch for local development, verify your Python version is at least 3.12:
```bash
python --version
```

## Installation Steps
1. Clone the repository fork:
   ```bash
   git clone https://github.com/DebasmitaBose0/AgentWatch-Ed.git
   ```
2. Navigate to the folder and install dependencies:
   ```bash
   cd AgentWatch
   pip install -e .[dev]
   ```
3. Run the verification test suite:
   ```bash
   python -m pytest tests/
   ```
