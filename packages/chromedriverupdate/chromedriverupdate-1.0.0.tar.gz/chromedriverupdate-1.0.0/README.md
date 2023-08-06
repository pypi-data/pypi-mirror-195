# chromedriverupdate

## Quick Start

```python

import os
from chromedriverupdate.chrome_driver import ChromeDriverUpdate

CHROME_DRIVER_PATH = '...'

def _browser():
    return webdriver.Chrome(
        # Your settings
    )

try:
    browser = _browser()
except SessionNotCreatedException as e:
    ChromeDriverUpdate(e.msg, os.path.dirname(CHROME_DRIVER_PATH)).update()
    browser = _browser()

```
