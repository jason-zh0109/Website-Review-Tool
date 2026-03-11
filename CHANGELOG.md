# **Changelog**

## [v3.0] - [03/11/2024]

### Added
  - Additional honeypot for the default admin endpoint to enhance security.
  - New documentation sections in the docs directory, including:
    - **Handover/:** Including cost estimation and deployment instructions.
    - **Product Requirements/:** Including architectural diagram, motivational model, personas, prototypes, and user stories.
    - **User Guide/:** Comprehensive user guide.
    - **Technical Specs/:** Including description of application layer, database, key algorithms, and key classes used.
  
### Updated
  - Various updates to existing documentation for clarity and completeness.

### Removed
- UoM logos to avoid any damage to the unimelb's reputation

---

## [v2.0] - [23/10/2024]
### Added
- Unique URLs for file downloads to prevent file overwriting during concurrent searches.
- Login-required authentication for search results and file downloads to ensure only authorized users can access files.
- Expiration periods for files to optimize memory usage and automatically delete files after timeout.
- Error message improvements for the signup process, ensuring correct content display.
- Static file configuration for AWS to optimize performance in cloud environments.

### Changed
- Updated forgot password functionality to verify both username and email for better security.
- Fixed internal server error when accessing the download URL with non-existing query parameters.
- Implemented a solution for arbitrary file read issues by avoiding direct user input for file types (concatenating `.xlsx`).

### Removed
- N/A

---

## [v1.0] - [18/10/2024]
### Added
- Initial release of the Website Review Tool with features for reviewing public websites and user registration.

### Changed
- N/A

### Removed
- N/A
