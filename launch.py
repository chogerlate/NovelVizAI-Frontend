#!/usr/bin/env python3
"""
Novel Companion AI Launcher
A convenient script to launch the Novel Companion AI application with optimal settings.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Novel Companion AI application."""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    app_path = project_root / "app" / "client.py"
    
    # Check if the app file exists
    if not app_path.exists():
        print(f"❌ Error: Application file not found at {app_path}")
        sys.exit(1)
    
    # Print welcome message
    print("🚀 Launching Novel Companion AI...")
    print("📚 Your intelligent reading assistant powered by advanced NLP")
    print("-" * 60)
    
    # Set environment variables for optimal Streamlit experience
    env = os.environ.copy()
    env.update({
        'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
        'STREAMLIT_BROWSER_SERVER_ADDRESS': '0.0.0.0',
        'STREAMLIT_BROWSER_SERVER_PORT': '8501',
    })
    
    # Build the command
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true",
    ]
    
    try:
        # Launch the application
        print(f"🔄 Starting Streamlit server...")
        print(f"🌐 Application will be available at: http://localhost:8501")
        print(f"📱 Network URL: http://0.0.0.0:8501")
        print("-" * 60)
        print("📋 Features available:")
        print("   • 📖 Intelligent Chapter Summarization")
        print("   • 👥 Dynamic Character Mapping") 
        print("   • 💬 Interactive Story Companion")
        print("   • 📊 Reading Analytics Dashboard")
        print("-" * 60)
        print("⚡ Press Ctrl+C to stop the server")
        print()
        
        # Run the application
        subprocess.run(cmd, env=env, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Thank you for using Novel Companion AI!")
        print("📚 Happy reading!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")
        sys.exit(1)
        
    except FileNotFoundError:
        print("❌ Error: Streamlit not found. Please install it with:")
        print("   pip install streamlit")
        print("   or")
        print("   uv add streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main() 