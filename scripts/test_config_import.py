import sys
import os

# Add the parent directory to the path so we can import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config   


print("✅ API URL:", config.API_BASE_URL)
print("✅ DB User:", config.DB_CONFIG["user"])
