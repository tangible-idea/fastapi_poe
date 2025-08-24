# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI application implementing the Poe protocol with additional Instagram integration and OpenAI endpoints. The project serves as both a FastAPI-based Poe bot server and a multi-service API gateway.

## Development Commands

### Package Management
- `pip install .` - Install the package and dependencies
- `pip install -r requirements.txt` - Install requirements directly

### Running the Application
- `python main.py` - Run the main FastAPI application on port 8000
- `python -m fastapi_poe` - Run as a Poe protocol server
- `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` - Run with auto-reload for development

### Testing
- `pytest` - Run all tests
- `pytest tests/test_types.py` - Run specific test file

### Code Quality
- `pre-commit run --all` - Run all pre-commit checks (Black formatting, Pyright type-checking, etc.)
- `pre-commit install` - Install pre-commit hooks for automatic checking

### Docker
- `docker build -t fastapi_poe .` - Build Docker image
- `docker run -p 8000:8000 fastapi_poe` - Run containerized application

## Architecture

### Core Components

**Main Application (`main.py`)**
- FastAPI app with CORS middleware
- Routes three main router modules: Instagram, Poe endpoints, OpenAI endpoints
- Health check endpoint at `/health`

**Poe Protocol Implementation (`fastapi_poe/`)**
- `base.py`: Core `PoeBot` class implementing the Poe protocol
- `types.py`: Pydantic models for protocol messages and responses
- `client.py`: Client for interacting with Poe services

**Service Endpoints**
- `instagram.py`: Instagram API integration with authentication and media upload
- `poe_endpoints.py`: Endpoints for various Poe bots (Llama, GPT-3, GPT-4)
- `openai_endpoints.py`: Direct OpenAI API integration with function calling

**Storage and Utilities**
- `storages.py`: `ClientStorage` class using TinyDB for Instagram session persistence
- `clientstorage.py`: Dependency injection for client storage
- `utils.py`: Utility functions for message concatenation and OpenAI API calls
- `db.json`: TinyDB database file for storing Instagram sessions

### Key Patterns

**Router-based Architecture**
The application uses FastAPI's router system to organize endpoints by service type (Instagram, Poe, OpenAI).

**Dependency Injection**
Instagram endpoints use FastAPI's dependency system with `ClientStorage` for session management.

**Async Generators**
Poe protocol implementation uses async generators for streaming responses via Server-Sent Events.

**Configuration via Environment**
- `POE_ACCESS_KEY`: Authentication key for Poe protocol
- `OPENAI_API_KEY`: OpenAI API authentication

## Development Notes

### Instagram Integration
- Uses `instagrapi` library for Instagram API access
- Session persistence via TinyDB in `db.json`
- Supports proxy, locale, and timezone configuration

### Poe Protocol
- Implements streaming responses with Server-Sent Events
- Supports various bot types (Llama, GPT variants)
- Authentication via Bearer tokens

### OpenAI Integration
- Direct API integration with function calling support
- Async wrapper around synchronous OpenAI client
- Error handling for API failures

### Code Style
- Uses Black for Python formatting (target Python 3.7+)
- Pyright for type checking
- Pre-commit hooks enforce code quality