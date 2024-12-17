# Errors and Exception Handling

## Overview

This document outlines the guidelines and best practices for handling exceptions in this project. The exception handling is structured across different layers to ensure clean, maintainable, and robust code.

## Layers of Exception Handling

### Repository Layer

- **Responsibility**: Interacts directly with the database.
- **Exception Handling**: No exceptions are handled at this layer. Any exceptions that occur are propagated to the service layer.

### Service Layer

- **Responsibility**: Contains business logic and interacts with the repository layer.
- **Exception Handling**: Captures all exceptions that may arise from the repository layer or within the service logic. These exceptions are then raised to the API/Route layer.

### API/Route Layer (Mutation, Query)

- **Responsibility**: Enables communication between the client and server by working directly with the service layer.
- **Exception Handling**: All exceptions raised by the service layer are captured by a centralized handler. This handler is defined as a decorator to keep the routes maintainable and clean.

## Custom Exception Handlers

We have defined some custom exception handlers to manage specific exceptions. These handlers must be used as they are.

### Example Custom Exception Handlers

- **InternalServerErrorException**: Raised for internal server errors.
- **NotFoundException**: Raised when a requested resource is not found.
- **BadRequestException**: Raised for bad requests.

### Using `CustomException`

For exceptions that do not have a predefined handler, use the `CustomException` class. This class `takes two arguments:

- `status_code`: The HTTP status code to be returned.
- `detail`: A detailed message about the exception.

## Example Usage

### Service Layer

```python
if existingEmail:
    raise CustomException(status_code=409, detail="Email already exist.")
```

This example is for conflicting resources.

## Conclusion

By following these guidelines, we ensure that our exception handling is consistent, maintainable, and effective across all layers of the application.

### N.B

All internal server errors has to be logged as error by using `logger.error` which is imported from `Config.logging`

#### Reference

If you need to read more about exception hundler, you can refer to the following [OFFICIAL PYTHON DOCUMENTATION](https://docs.python.org/3.12/tutorial/errors.html)
