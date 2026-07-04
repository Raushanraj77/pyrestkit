# Changelog

All notable changes to this project will be documented in this file.

This project follows Semantic Versioning (SemVer).

---

## [1.0.1] - 2026-07-05

### Added

* GitHub Actions CI workflow
* Makefile for development and quality checks
* Automated quality pipeline using Ruff, MyPy and Pytest
* Development and CI documentation

### Changed

* Refactored dependency management by separating runtime and development dependencies.
* Simplified project installation for contributors.
* Resolved dependency conflicts in GitHub Actions CI.
* Improved project reproducibility across clean environments.


---

## [1.0.0] - 2026-07-04

### Initial Release

#### Core

* API Client
* Request Builder
* Request Executor
* Session Management
* Business Clients

#### Authentication

* Basic Authentication
* Bearer Token Authentication
* API Key Authentication

#### Response

* FrameworkResponse
* ResponseBody
* Model Serialization

#### Assertions & Validation

* Fluent Assertions
* Status Code Validation
* Header Validation
* JSON Validation
* Response Time Validation
* JSON Schema Validation

#### Framework Features

* Retry Mechanism
* Hook System
* Factories
* Validators

#### Engineering

* Ruff
* MyPy
* Pytest
* Comprehensive Unit Tests
* Documentation
