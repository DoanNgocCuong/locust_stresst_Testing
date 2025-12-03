```bash
source .venv/bin/activate
```

```bash
uvicorn main:app --host 127.0.0.1 --port 25050 --reload --log-level debug
```
Cách trên ko mở localhost được 
```bash
uvicorn main:app --host 0.0.0.0 --port 25050 --reload --log-level debug
```
```bash
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)

logger = logging.getLogger("rag-backend")
```
