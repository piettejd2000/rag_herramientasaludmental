#!/usr/bin/env python3
"""
Emergency Rollback Script for RAG v2.0 → v1.0
Instantly restores v1.0 functionality if v2.0 deployment fails
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

def rollback_to_v1():
    """Rollback RAG v2.0 to v1.0 archived version."""
    
    print("🚨 EMERGENCY ROLLBACK TO RAG v1.0")
    print("=" * 50)
    
    # Paths
    current_dir = Path(__file__).parent
    v1_archive = current_dir / "v1.0_archive_20260609"
    
    # Check if archive exists
    if not v1_archive.exists():
        print("❌ ERROR: v1.0 archive not found!")
        print(f"Expected location: {v1_archive}")
        return False
    
    print(f"✅ Found v1.0 archive: {v1_archive}")
    
    # Create rollback backup of current v2.0
    rollback_backup = current_dir / f"v2.0_rollback_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        print("\n📦 Creating v2.0 backup...")
        rollback_backup.mkdir(exist_ok=True)
        
        # Backup current streamlit_app.py
        if (current_dir / "streamlit_app.py").exists():
            shutil.copy2(current_dir / "streamlit_app.py", rollback_backup / "streamlit_app.py")
            print("  ✅ Backed up streamlit_app.py")
        
        # Backup v2.0 directory
        if (current_dir / "v2.0").exists():
            shutil.copytree(current_dir / "v2.0", rollback_backup / "v2.0")
            print("  ✅ Backed up v2.0 directory")
        
        # Backup current requirements.txt
        if (current_dir / "requirements.txt").exists():
            shutil.copy2(current_dir / "requirements.txt", rollback_backup / "requirements_v2.txt")
            print("  ✅ Backed up requirements.txt")
        
    except Exception as e:
        print(f"⚠️  Backup failed: {e}")
        print("Continuing with rollback...")
    
    try:
        print("\n🔄 Restoring v1.0 files...")
        
        # Restore main streamlit app
        v1_main_app = v1_archive / "enhanced_streamlit_ui_cloud.py"
        if v1_main_app.exists():
            shutil.copy2(v1_main_app, current_dir / "streamlit_app.py")
            print("  ✅ Restored streamlit_app.py from v1.0")
        
        # Restore requirements.txt
        v1_requirements = v1_archive / "requirements.txt"
        if v1_requirements.exists():
            shutil.copy2(v1_requirements, current_dir / "requirements.txt")
            print("  ✅ Restored requirements.txt from v1.0")
        
        # Restore key v1.0 files
        key_files = [
            "enhanced_therapy_rag.py",
            "therapy_rag.py"
        ]
        
        for file in key_files:
            v1_file = v1_archive / file
            if v1_file.exists():
                shutil.copy2(v1_file, current_dir / file)
                print(f"  ✅ Restored {file}")
        
        # Restore chunking_pys if needed
        v1_chunking = v1_archive / "chunking_pys"
        current_chunking = current_dir / "chunking_pys"
        
        if v1_chunking.exists() and current_chunking.exists():
            # Backup current chunking_pys
            if (rollback_backup).exists():
                shutil.copytree(current_chunking, rollback_backup / "chunking_pys")
            
            # Restore v1.0 chunking_pys
            shutil.rmtree(current_chunking)
            shutil.copytree(v1_chunking, current_chunking)
            print("  ✅ Restored chunking_pys from v1.0")
        
        print("\n🎉 ROLLBACK SUCCESSFUL!")
        print("=" * 50)
        print("RAG v1.0 has been restored from archive")
        print(f"v2.0 backup saved to: {rollback_backup}")
        print("\nTo redeploy:")
        print("1. Test locally: streamlit run streamlit_app.py")
        print("2. If working, push to git for Streamlit Cloud deployment")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ROLLBACK FAILED: {e}")
        print("Manual intervention required!")
        return False

def validate_rollback():
    """Validate that rollback was successful."""
    print("\n🔍 Validating rollback...")
    
    current_dir = Path(__file__).parent
    
    # Check key files exist
    key_files = [
        "streamlit_app.py",
        "requirements.txt", 
        "enhanced_therapy_rag.py"
    ]
    
    missing_files = []
    for file in key_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All key files present")
    
    # Check if streamlit_app.py is v1.0 (should not contain v2.0 references)
    app_file = current_dir / "streamlit_app.py"
    with open(app_file, 'r') as f:
        content = f.read()
    
    v2_indicators = ['RAG v2.0', 'adaptive_router', 'PATH_A', 'PATH_B', 'PATH_C']
    v2_found = any(indicator in content for indicator in v2_indicators)
    
    if v2_found:
        print("⚠️  streamlit_app.py still contains v2.0 references")
        return False
    
    print("✅ streamlit_app.py appears to be v1.0")
    print("✅ Rollback validation successful")
    return True

if __name__ == "__main__":
    print("RAG Emergency Rollback Script")
    print("This will restore the v1.0 system from archive")
    print("=" * 50)
    
    response = input("Are you sure you want to rollback to v1.0? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        success = rollback_to_v1()
        
        if success:
            validate_rollback()
        else:
            print("\nRollback failed. Manual restoration may be required.")
            sys.exit(1)
    else:
        print("Rollback cancelled.")
        sys.exit(0)