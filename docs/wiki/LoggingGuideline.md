# Error Logging Guideline

All internal server errors has to be logged by `logger.error` which is set up in `Config.logging` file on the root directory of the project.

You can use it by simply importing it like this 

```python
from config.Config import logger
```

and be able to access logg levels like `logger.info`

## Related Documentation

- [Errors and Exception Handling](./ExceptionHandling.md)
