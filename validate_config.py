#!/usr/bin/env python3
"""
Validation script for Railway deployment configuration
Check if all required environment variables and configurations are set
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add code directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))

async def validate_configuration():
    """Validate all required configurations for Railway deployment"""
    
    print("🔍 Validating Railway deployment configuration...")
    
    # Load environment variables
    load_dotenv(os.path.join('code', '.env'))
    
    errors = []
    warnings = []
    
    # Check OpenAI configuration
    print("\n📋 Checking OpenAI configuration...")
    openai_key = os.getenv('OPENAI_API_KEY')
    openai_endpoint = os.getenv('OPENAI_ENDPOINT')
    
    if not openai_key:
        errors.append("❌ OPENAI_API_KEY not found in environment")
    elif not openai_key.startswith('sk-'):
        errors.append("❌ OPENAI_API_KEY format invalid (should start with 'sk-')")
    else:
        print("✅ OPENAI_API_KEY found")
        
    if not openai_endpoint:
        warnings.append("⚠️ OPENAI_ENDPOINT not set, using default")
    else:
        print("✅ OPENAI_ENDPOINT configured")
    
    # Check Qdrant configuration
    print("\n📋 Checking Qdrant configuration...")
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_key = os.getenv('QDRANT_API_KEY')
    
    if not qdrant_url:
        errors.append("❌ QDRANT_URL not found - Qdrant Cloud required for Railway")
    elif not qdrant_url.startswith('https://'):
        errors.append("❌ QDRANT_URL should be HTTPS URL")
    else:
        print("✅ QDRANT_URL configured")
        
    if not qdrant_key:
        warnings.append("⚠️ QDRANT_API_KEY not set (may be optional)")
    else:
        print("✅ QDRANT_API_KEY configured")
    
    # Check config files
    print("\n📋 Checking configuration files...")
    config_files = [
        'code/config/config_retrieval.yaml',
        'code/config/config_llm.yaml',
        'code/config/config_embedding.yaml'
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} exists")
        else:
            errors.append(f"❌ {config_file} not found")
    
    # Check retrieval configuration specifically
    try:
        with open('code/config/config_retrieval.yaml', 'r') as f:
            content = f.read()
            if 'preferred_endpoint: qdrant_url' in content:
                print("✅ Retrieval configured for Qdrant Cloud")
            elif 'preferred_endpoint: qdrant_local' in content:
                warnings.append("⚠️ Still using qdrant_local - should change to qdrant_url for Railway")
            else:
                warnings.append("⚠️ Retrieval endpoint configuration unclear")
    except Exception as e:
        errors.append(f"❌ Error reading retrieval config: {e}")
    
    # Check required files
    print("\n📋 Checking required files...")
    required_files = [
        'requirements.txt',
        'railway.json',
        'nixpacks.toml',
        'start.sh'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            errors.append(f"❌ {file} not found")
    
    # Test imports
    print("\n📋 Testing key imports...")
    try:
        from config.config import CONFIG
        print("✅ CONFIG module imported successfully")
    except Exception as e:
        errors.append(f"❌ Error importing CONFIG: {e}")
    
    try:
        from retrieval.retriever import get_vector_db_client
        print("✅ Vector DB client import successful")
    except Exception as e:
        errors.append(f"❌ Error importing vector DB client: {e}")
    
    # Summary
    print("\n" + "="*50)
    print("📊 VALIDATION SUMMARY")
    print("="*50)
    
    if not errors:
        print("🎉 ✅ All validations passed!")
        if warnings:
            print("\n⚠️ Warnings:")
            for warning in warnings:
                print(f"   {warning}")
        return True
    else:
        print("💥 ❌ Validation failed!")
        print("\n🚨 Errors:")
        for error in errors:
            print(f"   {error}")
        
        if warnings:
            print("\n⚠️ Warnings:")
            for warning in warnings:
                print(f"   {warning}")
        
        print("\n📋 Next steps:")
        print("1. Fix all errors listed above")
        print("2. Set environment variables in Railway dashboard")
        print("3. Update configuration files as needed")
        print("4. Re-run this validation script")
        
        return False

def main():
    """Main function"""
    try:
        success = asyncio.run(validate_configuration())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
