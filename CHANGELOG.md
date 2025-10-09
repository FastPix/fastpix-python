# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---
## [1.0.1]

### Fixed
- Fixed all error handling links in README.md documentation
  - Corrected typos in file paths (e.g., `fFastpix` → `Fastpix`)
  - Updated filenames to match actual error class files (added missing underscores)
  - Fixed 23 error class links to properly redirect to correct files
  - Verified all links now point to existing files in `src/Fastpix/errors/` directory

## [1.0.0]

### Added
- Complete API coverage for Media, Live Streaming, Video Data, and Signing Keys
- Python 3.9+ support with async/await patterns and type hints
- Media upload, management, and processing capabilities
- Live streaming with simulcasting support
- Video analytics and performance tracking
- Cryptographic signing keys for secure authentication
- In-video AI processing features
- DRM configuration and management
- Playlist creation and management
- Comprehensive error handling with specific exception types
- Both sync and async client implementations
- Built-in retry mechanisms and timeout handling

### Changed
- Reorganized package structure for better maintainability
- Updated dependencies to modern Python packages (httpx, pydantic, httpcore)
- Improved API design with better error handling
- Enhanced documentation and examples

### Fixed
- Improved error handling with specific exception types
- Fixed type annotation issues for better IDE support
- Ensured consistent API patterns across modules

---

## [0.1.8]

### Added
- Enhanced README documentation with comprehensive usage examples
- Improved project setup and installation instructions

### Changed
- Updated version number to reflect latest improvements
- Restructured documentation for better user experience
- Enhanced code examples and API usage guides

---

## [0.1.7]

### Added
- New base URL configuration system for better API connectivity
- Support for different API environments (production, staging, development)

### Changed
- Updated base URL configuration for improved API endpoint resolution
- Enhanced connection stability and reliability
- Improved error handling for connection issues

---

## [0.1.6]

### Added
- Project URL management system for better package distribution
- Enhanced package metadata and configuration

### Changed
- Updated project URLs in configuration files for better package identification
- Improved package metadata and distribution information
- Enhanced project discoverability and documentation links

---

## [0.1.5]

### Added
- Comprehensive version tracking and file management system
- Automated version control and release management
- Initial project structure and configuration framework

### Changed
- Updated version number and project configuration
- Improved project organization and file structure
- Enhanced build and deployment processes

---

## [0.1.4]

### Added
- New package naming convention for better identification
- Enhanced package metadata and distribution information

### Changed
- Changed package name for better identification and distribution
- Updated package metadata and configuration
- Improved package discoverability and installation process

---

## [0.1.3]

### Added
- Version management improvements
- Enhanced configuration system

### Changed
- Updated version number to reflect latest changes
- Improved project configuration and build processes
- Enhanced package metadata and dependencies

---

## [0.1.2]

### Added
- Comprehensive documentation link validation system
- Enhanced workflow automation and CI/CD pipeline

### Fixed
- Corrected redirection links in README documentation
- Fixed broken documentation links for better user experience
- Resolved navigation issues in project documentation

### Changed
- Updated workflow configuration and processes
- Improved project automation and deployment pipeline
- Enhanced documentation structure and organization

---

## [0.1.1]

### Changed
- Updated codebase with consistent naming conventions
- Added comprehensive package description

### Fixed
- Resolved naming convention inconsistencies

---

## [0.1.0]

### Added
- Initial release of FastPix Python SDK
- Sync and async client support
- Media API integration with upload, management, and processing
- Playback ID management for media files
- Media operations (list, get, update, delete)
- Presigned URL generation for video uploads
- Livestream API integration
- Livestream management (create, update, delete)
- Playback ID management for livestreams
- Simulcast configuration for livestreams