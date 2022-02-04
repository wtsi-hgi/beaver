# Beaver Design Document

With special thanks to Christoper Harrison for their original design ideas [on Confluence](https://confluence.sanger.ac.uk/display/HGI/3.+Design).

## Development Criteria

- The system will be written in Python 3.8 or newer for the backend process, and a React framework for the frontend.
- The test suite must pass without issues.
- The system's code must be type annotated (`strict` type checking is recommended)
- The Python code must conform to the PEP8 style
- All commits must follow a standard specification (defined later)
- The various parts of the application will be deployed together using `docker-compose`.
- As the parts will be deployed together, it is acceptable to define the build steps in the compose file.

## Source Control

- git will be used for source control, `origin` will be hosted by GitHub
- The default branch will be named `main`
- Feature branches will branch from `main` and be named `feature/DESC` where `DESC` is a description
- Bugs and issues will be entered into the GitHub issues page
- Fix branches will branch from `main` and be named `fix/DESC` where `DESC` is a description
- Commits will be small and done regularly

### Commit Message Template

```
Short description of the commit

Added:
* List of added functionality
* ...

Removed:
* List of removed functionality
* ...

Changed:
* List of changed functionality
* ...

Fixed:
* List of fixed functionality
* ...
```

- Any of the lists can be removed if they're empty
- Ideally, each list should contain only one or two items, with no more than five items across all lists; any more implies the commit it too large and should be done more frequently.
- If any item in the Fixed list refers to a GitHub issue, include the text (resolves #ISSUE_ID), where ISSUE_ID is the GitHub issue number.

