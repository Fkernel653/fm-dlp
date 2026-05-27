# re-kiss — A powerful set of tools for working with regular expressions

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/re-kiss.svg)](https://pypi.org/project/re-kiss/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-261230?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)

An elegant and intuitive toolkit that makes regex operations simple and smooth. Provides comprehensive functions for validation, extraction, and cleaning of data using regular expressions in Python.

## 🚀 Quick Start

```bash
pip install re-kiss          # Requires Python 3.7+
```

```python
from re_kiss import validate_email, extract_emails, strip_html

# Validation
print(validate_email("user@example.com"))  # True

# Extraction
text = "Contact: john@mail.com and jane@site.ru"
print(extract_emails(text))  # ['john@mail.com', 'jane@site.ru']

# Cleaning
html = "<p>Hello <b>World</b></p>"
print(strip_html(html))  # "Hello World"
```

## 📋 Modules

### `validators` — Validate data
```python
from re_kiss import validate_email, validate_url, validate_phone, validate_password, validate_ip, validate_date
```
| Function | Description |
|----------|-------------|
| `validate_email(email, strict=True)` | Email address validation |
| `validate_url(url, require_https=False)` | URL validation |
| `validate_phone(phone, locale='any')` | Phone number validation (`'us'`, `'uk'`, `'any'`) |
| `validate_password(password, min_length=8, ...)` | Password strength with configurable rules |
| `validate_ip(ip, version=4)` | IPv4/IPv6 validation |
| `validate_date(date_str, format='iso')` | Date validation (`'iso'`, `'us'`, `'eu'`) |

### `extractors` — Extract data from text
```python
from re_kiss import extract_emails, extract_urls, extract_phones, extract_numbers, extract_words, extract_between
```
| Function | Description |
|----------|-------------|
| `extract_emails(text, unique=True)` | Extract email addresses |
| `extract_urls(text, unique=True)` | Extract URLs |
| `extract_phones(text, locale='any')` | Extract phone numbers |
| `extract_numbers(text, decimals=True, negative=True)` | Extract numbers (int/float) |
| `extract_words(text, min_length=1, language='all')` | Extract words (`'en'`, `'ru'`, `'all'`) |
| `extract_between(text, start, end, include_bounds=False)` | Extract text between markers |

### `cleaners` — Clean and normalize text
```python
from re_kiss import strip_html, normalize_whitespace, remove_special_chars, remove_numbers, remove_punctuation
```
| Function | Description |
|----------|-------------|
| `strip_html(text, keep_content=True)` | Remove HTML tags |
| `normalize_whitespace(text)` | Collapse multiple spaces/newlines |
| `remove_special_chars(text, keep_spaces=True, ...)` | Remove special characters |
| `remove_numbers(text, keep_positions=False, replacement='')` | Remove numbers |
| `remove_punctuation(text, keep_sentences=True)` | Remove punctuation |

## 📖 Examples

```python
from re_kiss import *

# Email validation
validate_email("user@example.com")           # True
validate_email("invalid-email")              # False
validate_email("test@mail", strict=False)    # True (loose mode)

# Password strength
validate_password("Weak")                    # False
validate_password("Str0ng!Pass", 
                  min_length=8,
                  require_special=True)      # True

# Extract numbers
extract_numbers("Price: $19.99, Qty: 5")    # [19.99, 5]
extract_numbers("No decimals here", 
                decimals=False)              # []

# Extract between markers
extract_between("hello {world} foo", 
                "{", "}")                    # ['world']
extract_between("<!-- comment -->", 
                "<!--", "-->")              # [' comment ']

# HTML cleaning
strip_html("<p>Hello <b>World</b></p>")     # "Hello World"
strip_html("<div>Text</div>", 
           keep_content=False)               # ""

# Text normalization
normalize_whitespace("Hello    world!\t\n")  # "Hello world!"
remove_special_chars("User123! $pecial")     # "User pecial"
remove_punctuation("Hello, world!")          # "Hello world"
```

### Advanced — RegexPattern class
```python
from re_kiss import RegexPattern

# Create reusable pattern
pattern = RegexPattern(r'\b[A-Z][a-z]+\b')
pattern.findall("Alice Bob and Charlie")     # ['Alice', 'Bob', 'Charlie']

# Quick test
pattern.test("No names here")                # False

# Count matches
pattern.count("Alice Bob Charlie")           # 3

# Replace with function
pattern.replace("Alice Bob", str.upper)      # "ALICE BOB"

# Iterator with positions
for match in pattern.finditer("Alice Bob"):
    print(match.text, match.start, match.end)
# Alice 0 5
# Bob 6 9
```

## 🔧 Dependencies

| Library | Purpose |
|---------|---------|
| **Python Standard Library** | `re`, `typing`, `dataclasses` |

Zero external dependencies — uses only built-in Python modules.

## ❓ FAQ

**Why re-kiss over raw `re`?** Simplifies common regex tasks into clean, readable functions with sensible defaults. No more writing boilerplate patterns for emails, URLs, phone numbers.

**Performance impact?** Minimal. Patterns are compiled once and cached. The `RegexPattern` class wraps `re.compile` with a cleaner interface.

**Unicode support?** Full Unicode support via `re.UNICODE` flag. Works with Cyrillic, Latin, and other alphabets.

**Custom patterns?** Use `RegexPattern` class or pass custom strings to any function that accepts patterns.

## 📄 License

MIT License — see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- Python's `re` module — The foundation
- Inspired by common regex patterns used in web scraping and data validation

---

**Author:** [Fkernel653](https://github.com/Fkernel653)
**Repository:** [github.com/Fkernel653/re-kiss](https://github.com/Fkernel653/re-kiss)
**PyPI:** [pypi.org/project/re-kiss](https://pypi.org/project/re-kiss/)
