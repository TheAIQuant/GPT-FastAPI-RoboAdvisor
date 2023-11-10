# Robo Advisor with Chat GPT and FastAPI

## Overview

This project demonstrates the creation of a Robo Advisor using Chat GPT from OpenAI and FastAPI. The Robo Advisor can provide investment advice based on real-time financial news and data.

## Features

- Real-time financial news analysis
- Trend analysis generation
- FastAPI web service for user interaction

## Prerequisites

Before running the project, make sure you have the following prerequisites:

- Python 3.x
- OpenAI API key
- Finnhub API key
- FastAPI (can be installed via requirements.txt)
- Other required dependencies (can be installed via requirements.txt)
- The `finnlp` and `finrl-meta` repositories (Please clone these repositories inside this project's directory)

```plaintext
git clone https://github.com/AI4Finance-Foundation/FinNLP
git clone https://github.com/AI4Finance-Foundation/FinRL-Meta
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/robo-advisor.git
   cd robo-advisor
   ```

Clone the required repositories for integration (FinNLP and FinRL-Meta) inside your project repository:
```bash
git clone https://github.com/AI4Finance-Foundation/FinNLP
git clone https://github.com/AI4Finance-Foundation/FinRL-Meta
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Create a .env file with your OpenAI and Finnhub API keys:
```plaintext
OPENAI_API_KEY=your_openai_api_key
FINNHUBAPI_KEY=your_finnhub_api_key
```

Run the FastAPI application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The Robo Advisor will be accessible at http://127.0.0.1:8000.
