# string_validator

A fast and correct Python string validator library. Also includes a [cuid](https://github.com/paralleldrive/cuid) generator for the sake of posterity.

Validates:

- Emails
- IP addresses
- IPv4 addresses
- IPv6 addresses
- URLs
- Credit card numbers
- Phone numbers
- Non-control characters

## Example

```python
import string_validator

result = string_validator.validate_email("example@example.com")
assert result == True
```
