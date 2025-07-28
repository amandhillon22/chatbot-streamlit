# Chatbot Diya - Project Structure

This document explains the organized folder structure of the Chatbot Diya project.

## 📁 Project Structure Overview

```
chatbot-diya/
├── 📁 src/                          # Main source code
│   ├── 📁 core/                     # Core business logic
│   ├── 📁 nlp/                      # Natural Language Processing
│   ├── 📁 database/                 # Database utilities
│   └── 📁 api/                      # Web API and services
├── 📁 tests/                        # All test files
│   ├── 📁 unit/                     # Unit tests
│   ├── 📁 integration/              # Integration tests
│   └── 📁 e2e/                      # End-to-end tests
├── 📁 scripts/                      # Utility scripts
│   ├── 📁 deployment/               # Deployment scripts
│   └── 📁 database/                 # Database setup scripts
├── 📁 frontend/                     # Web interface
├── 📁 docs/                         # Documentation
│   ├── 📁 features/                 # Feature documentation
│   └── 📁 fixes/                    # Bug fix documentation
├── 📁 data/                         # Data files and schemas
├── 📁 logs/                         # Application logs
└── 📁 config files                  # Configuration files
```

## 📦 Package Details

### 🔧 `src/core/` - Core Engine
**Purpose**: Contains the main business logic and core functionality

**Key Files**:
- `intelligent_reasoning.py` - Main AI reasoning engine
- `query_agent.py` - Primary query processing agent
- `query_agent_enhanced.py` - Enhanced query processing with advanced features
- `sql.py` - SQL generation and database interaction
- `config.py` - Application configuration management
- `user_manager.py` - User session and authentication management
- `performance_monitor.py` - System performance tracking

**What it does**:
- Processes user queries and converts them to SQL
- Manages business logic for complaint handling, plant management, etc.
- Handles database connections and query execution
- Monitors system performance and user sessions

### 🧠 `src/nlp/` - Natural Language Processing
**Purpose**: Handles understanding and processing of user natural language input

**Key Files**:
- `enhanced_pronoun_resolver.py` - Resolves pronouns in follow-up questions ("show their details")
- `enhanced_table_mapper.py` - Maps user queries to appropriate database tables
- `sentence_embeddings*.py` - Text similarity and semantic understanding
- `embeddings.py` - Core embedding functionality
- `create_lightweight_embeddings.py` - Optimized embedding creation

**What it does**:
- Understands user intent from natural language
- Resolves pronouns and contextual references
- Maps queries to database entities
- Provides semantic similarity matching

### 🗄️ `src/database/` - Database Utilities
**Purpose**: Database-related utilities and data processing

**Key Files**:
- `database_reference_parser.py` - Parses database schema and relationships
- `distance_units.py` - Handles distance unit conversions
- `eoninfotech_masker.py` - Data masking for sensitive information

**What it does**:
- Parses and understands database structure
- Handles data transformations and conversions
- Provides data security and masking capabilities

### 🌐 `src/api/` - Web API and Services
**Purpose**: Web interface and external service integrations

**Key Files**:
- `app.py` - Main Flask application entry point
- `flask_app.py` - Flask web application with routes
- `llm_service.py` - Integration with Large Language Models (LLM)

**What it does**:
- Provides web API endpoints for the chatbot
- Handles HTTP requests and responses
- Integrates with external AI services

## 🧪 `tests/` - Testing Framework

### `tests/unit/` - Unit Tests
- Tests individual functions and methods
- Fast, isolated tests
- Examples: `test_enhanced_pronoun_resolution.py`, `test_embeddings.py`

### `tests/integration/` - Integration Tests
- Tests component interactions
- Database integration tests
- Examples: `test_final_integration.py`, `test_integration_summary.py`

### `tests/e2e/` - End-to-End Tests
- Full system workflow tests
- User scenario testing
- Examples: `test_chatbot_e2e.py`, `test_live_conversation.py`

## 🚀 `scripts/` - Utility Scripts

### `scripts/deployment/` - Deployment
- `deploy.sh` - Main deployment script
- `start_*.sh` - Various startup scripts for different environments
- `restart_*.sh` - Service restart scripts

### `scripts/database/` - Database Management
- `setup_database.py` - Database initialization
- `generate_db_doc.py` - Generate database documentation
- `setup_optimizations.sh` - Database performance optimization

### Other Scripts
- `run_*.py` - Various test runners and utilities
- `simple_*.py` - Simplified versions for testing

## 🎨 `frontend/` - User Interface
- `index.html` - Main web interface
- `script.js` - Frontend JavaScript logic
- `styles.css` - UI styling
- `feedback-system.js` - User feedback collection
- `memory-system.js` - Conversation memory management

## 📚 `docs/` - Documentation

### `docs/features/` - Feature Documentation
- `crm_complaint_system_definition.md` - Complaint system overview
- `database_reference.md` - Database structure reference
- `ship_to_address_definition.md` - Address handling system

### `docs/fixes/` - Bug Fix Documentation
- Various markdown files documenting fixes and improvements
- Historical record of system enhancements

### Main Documentation
- `SETUP_GUIDE.md` - Project setup instructions
- `OPTIMIZATION_GUIDE.md` - Performance optimization guide
- `LAN_ACCESS_GUIDE.md` - Network access configuration

## 💾 `data/` - Data Files
- `database_schema.sql` - Database schema definition
- `cookies.txt` - Session data
- `FIX_SUMMARY.py` - Summary of system fixes

## 📊 `logs/` - Application Logs
- `performance.log` - System performance logs
- `app.log` - Application logs
- `flask.log` - Web server logs
- `server.log` - Server operation logs

## ⚙️ Configuration Files (Root Level)
- `requirements.txt` - Python dependencies
- `config.py` - Main configuration
- `.env*` - Environment variables
- `Procfile` - Deployment configuration
- `README.md` - Project overview

## 🎯 How to Navigate the Project

### For New Developers:
1. **Start with** `docs/SETUP_GUIDE.md` for initial setup
2. **Understand the core** by reading `src/core/intelligent_reasoning.py`
3. **See how queries work** in `src/core/query_agent.py`
4. **Check the web interface** in `src/api/flask_app.py`

### For Debugging:
1. **Check logs** in `logs/` directory
2. **Run unit tests** from `tests/unit/`
3. **Use debug scripts** in `scripts/`

### For Adding Features:
1. **Core logic** goes in `src/core/`
2. **NLP features** go in `src/nlp/`
3. **Database utilities** go in `src/database/`
4. **API endpoints** go in `src/api/`
5. **Always add tests** in appropriate `tests/` subdirectory

### For Deployment:
1. **Use scripts** in `scripts/deployment/`
2. **Check configuration** files in root
3. **Review logs** after deployment

This organized structure makes the project much easier to understand, maintain, and extend! 🚀
