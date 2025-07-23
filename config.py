"""
Configuration settings for development and production environments
"""

class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgresql://postgres:Akshit@123@localhost:5432/rdc_dump'
    SECRET_KEY = 'diya-chatbot-secret-key-change-in-production'

class DevelopmentConfig(Config):
    DEBUG = True
    HOST = 'localhost'
    PORT = 5000

class ProductionConfig(Config):
    DEBUG = False
    HOST = '10.217.63.71'  # Your network IP address
    PORT = 5050  # Different port for production
