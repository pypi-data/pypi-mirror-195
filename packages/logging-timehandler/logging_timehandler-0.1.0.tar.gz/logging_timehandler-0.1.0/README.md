Log files are generated based on the time and the latest n logs are automatically retained

# Example

```python
import logging
import logging_timehandler

logger = logging.getLogger(__name__)
handler = logging_timehandler.TimeHandler('./log/%Y_%m_%d/%Y_%m_%d_%S.txt', retain=5)
handler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

for i in range(10):
    logger.info('hello')
```