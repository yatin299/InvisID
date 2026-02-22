# InvisID - Leak Attribution System for Sensitive Images
## Trace Leaked Product Designs Back to the Source Employee

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

InvisID is a **leak attribution system** that traces leaked sensitive images back to the source employee using invisible watermarking.

---

## The Problem

Your company shares sensitive product designs internally. If an image leaks to the press or competitors, how do you find the source?

## The Solution: InvisID

InvisID traces leaks by embedding a unique, encrypted Employee ID into images **at the moment an employee downloads them**. If that image later surfaces externally, scan it to decode the watermark and identify the leaker.

### How It Works

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  1. ADMIN UPLOADS                                                           │
│     Company uploads sensitive product design images                          │
│                                                                              │
│  2. EMPLOYEE DOWNLOADS                                                      │
│     Employee requests to download image                                      │
│     ↓                                                                       │
│     System invisibly embeds their unique Employee ID                         │
│     ↓                                                                       │
│     Employee receives watermarked image                                      │
│                                                                              │
│  3. IMAGE LEAKS                                                             │
│     Leaked image found on social media/press                                 │
│                                                                              │
│  4. TRACE SOURCE                                                            │
│     Admin uploads leaked image → System extracts ID → Identifies leaker       │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Key Features

🔐 **Military-Grade Security**
- AES-256-GCM encryption with PBKDF2 key derivation
- API Key authentication (admin + employee)
- Cryptographically chained audit logs (tamper-evident)
- Rate limiting (10 req/min)

🎯 **Research-Grade Steganography**
- DWT-DCT-SVD hybrid algorithm (more robust than basic DWT+DCT)
- Adaptive strength based on image complexity
- Survives JPEG compression, noise, basic filtering
- DWT+DCT hybrid algorithm via `invisible-watermark` library
- Survives JPEG compression, noise
- Attack Simulation Dashboard (50+ scenarios)

🌐 **Complete Web Application**
- FastAPI backend with auto-generated docs
- Admin dashboard for uploads and investigation
- Employee download portal
- Audit log viewer

---

## How It Works

### When Employee Downloads an Image:
```
Employee requests download
        │
        ▼
Auth verifies employee (from API key)
        │
        ▼
AES-256-GCM Encryption (encrypts Employee ID)
        │
        ▼
DWT+DCT Steganography (embeds encrypted ID into image)
        │
        ▼
Employee receives watermarked image
        │
        ▼
AUDIT LOG: "EMP-007 downloaded design_v2.png at 2026-02-22 10:30:00"
```

### When Investigating a Leak:
```
Company finds leaked image online
        │
        ▼
Admin uploads to InvisID system
        │
        ▼
DWT+DCT Extraction (extracts hidden data)
        │
        ▼
AES-256-GCM Decryption (reveals Employee ID)
        │
        ▼
"Employee ID: EMP-007"
        │
        ▼
Cross-reference with audit logs to confirm
```

### Scope & Limitations

**In Scope:**
- Digital data exfiltration (email, USB, cloud upload)
- JPEG/PNG compression attacks (Quality 50+)
- Gaussian noise and basic image filtering
- Accidental sharing and casual leaks

**Out of Scope:**
- Screen capture / screenshot attacks
- Physical photography of screens (Analog Hole)
- Severe cropping (>30%)
- Print-scan attacks
- AI-based adversarial watermark removal

**Why Invisible?**
Unlike visible watermarks that alert attackers to their presence, InvisID's invisible watermark operates covertly. Employees don't know tracking data is embedded, eliminating the motivation to remove it. This addresses accidental sharing and casual social media posting.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern web framework with auto-docs |
| **invisible-watermark** | DWT+DCT steganography library |
| **PyCryptodome** | AES-256-GCM encryption |
| **Pillow** | Image processing |
| **UV** | Python package management |

---

## Installation

### Prerequisites
- Python 3.11+
- UV package manager

### Setup

```bash
# 1. Install UV
pip install uv

# 2. Clone the repository
git clone https://github.com/your-team/invisid.git
cd invisid

# 3. Install dependencies
uv sync

# 4. Set up environment variables
copy .env.example .env

# 5. Run the application
uv run uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

### Environment Variables

```env
# Admin API key (for security team)
ADMIN_API_KEY=your-admin-key

# Employee API key (for employees)
EMPLOYEE_API_KEY=your-employee-key

# Master secret for PBKDF2 key derivation (not the actual encryption key)
MASTER_SECRET=your-root-secret-minimum-32-chars

# Unique salt per deployment (generate with: openssl rand -hex 16)
SALT=your-unique-salt

# Debug mode
DEBUG=false

# Log level
LOG_LEVEL=INFO
```

**Security Note:** We store a master secret, not the actual encryption key. The AES-256 key is derived at runtime using PBKDF2 with 100,000 iterations. This prevents key compromise from static file leaks.

**Never commit `.env` to git!**

---

## Usage

### Admin Workflow (Security Team)

1. **Upload Master Images:**
   - POST to `/api/admin/upload`
   - Upload sensitive product design images

2. **View Download History:**
   - GET `/api/admin/logs`
   - See which employee downloaded which image and when

3. **Investigate a Leak:**
   - POST `/api/investigate`
   - Upload the leaked image
   - Get decrypted employee ID

### Employee Workflow

1. **List Available Images:**
   - GET `/api/images`

2. **Download:**
   - GET `/api/images/{id}/download`
   - Receives watermarked image automatically

---

## API Endpoints

### Admin Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/admin/upload` | POST | Upload master image |
| `/api/admin/images` | GET | List available images |
| `/api/admin/images/{id}` | DELETE | Delete image |
| `/api/admin/logs` | GET | View download history |
| `/api/investigate` | POST | Extract ID from leaked image |

### Employee Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/images` | GET | List available images |
| `/api/images/{id}/download` | GET | Download with watermark embed |

### Attack Simulation

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/attack/run` | POST | Run attack simulation |

### Health

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API documentation |

### API Example

```bash
# Download watermarked image (employee)
curl -X GET "http://localhost:8000/api/images/img_001/download" \
  -H "X-API-Key: your-employee-key" \
  --output watermarked.png

# Investigate a leak (admin)
curl -X POST "http://localhost:8000/api/investigate" \
  -H "X-API-Key: your-admin-key" \
  -F "file=@leaked.png"
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENTS                                            │
│   ┌──────────────────┐                      ┌──────────────────┐         │
│   │  Admin Browser   │                      │ Employee Browser  │         │
│   └────────┬─────────┘                      └────────┬─────────┘         │
│            │ HTTP + API Key                           │ HTTP + API Key    │
└────────────┼──────────────────────────────────────────┼───────────────────┘
             │                                            │
             ▼                                            ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND                                     │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      SECURITY LAYER                                    │  │
│  │  API Key Auth  │  Rate Limiter  │  Input Validator  │  Headers      │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      CORE SERVICES                                     │  │
│  │  Auth Service  │  Image Service │  Stego Service  │  Audit Service  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
             │                                            │
             ▼                                            ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  Master Images  │   │   Audit Logs   │   │   Config       │
│   (storage/)    │   │   (logs.json)  │   │   (.env)       │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

---

## Project Structure

```
invisid/
├── app/
│   ├── main.py                    # FastAPI app
│   ├── config.py                  # Settings
│   ├── dependencies/              # Auth, rate limiting
│   ├── middleware/                # Security headers
│   ├── routers/                   # API endpoints
│   │   ├── admin.py              # Admin endpoints
│   │   ├── images.py             # Image endpoints
│   │   ├── investigate.py        # Leak investigation
│   │   └── attack.py             # Attack simulation
│   ├── services/                  # Business logic
│   │   ├── auth_service.py
│   │   ├── image_service.py
│   │   ├── stego_service.py
│   │   ├── crypto_service.py
│   │   └── audit_service.py
│   ├── models/                    # Pydantic schemas
│   └── utils/                     # File validation
├── stego/                         # Watermarking module
├── crypto/                        # Encryption module
├── storage/                       # Image storage
│   ├── master/                   # Original images
│   └── temp/                     # Temporary files
├── logs/                         # Audit logs
├── tests/                        # Test files
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Security (SSDLC + STRIDE)

This project follows **Secure Software Development Lifecycle** principles:

- **Threat Modeling**: STRIDE framework for identifying security risks
- **Secure Coding**: Input validation, authentication, audit logging
- **Security Testing**: Bandit, pip-audit, Gitleaks in CI pipeline

### Key Security Features

| Feature | Implementation |
|---------|----------------|
| **Key Derivation** | PBKDF2 (100K iterations) - key derived at runtime |
| **Audit Logs** | Cryptographically chained + external anchor (tamper-evident) |
| **Encryption** | AES-256-GCM with PBKDF2 key derivation |
| **Key Management** | Separation of Secrets + Key Epochs (30-day rotation) |
| **Authentication** | API Key-based (admin + employee roles) |
| **Rate Limiting** | 10 requests/minute per API key |

### Authentication

All endpoints require `X-API-Key` header:
- Admin API key for uploads, logs, investigation
- Employee API key for downloads

### Key Security Features

| Feature | Implementation |
|---------|----------------|
| **PBKDF2 Key Derivation** | Master secret from .env → derives AES-256 key at runtime |
| **Separation of Secrets** | Master secret (`.env`) + unique salt per watermark (database) |
| **Key Epochs** | 30-day rotation - compromised epoch can't decrypt old watermarks |
| **Log Chaining** | Each log hashes previous entry - tampering breaks chain |
| **External Anchor** | Daily root hash published to WORM store (Gist/S3) |

### Why PBKDF2 + Separation?

> "An attacker who steals `.env` gets a useless Master Secret. An attacker who steals the database gets useless Salts. They must breach BOTH to attempt decryption."

### Why Log Chaining + External Anchor?

> "A rogue admin could delete all logs and rewrite history. Our daily cron job publishes the root hash to an immutable external store. If anyone alters historical logs, the chain breaks and won't match the external anchor."

### Privacy

This tool monitors employee activity. In production:
- 90-day data retention policy
- Explicit employee monitoring disclosure required
- Crypto-shredding after retention period

---

## Development

### Running Tests

```bash
uv run pytest
uv run pytest -v
```

### Running the App

```bash
uv run uvicorn app.main:app --reload
```

---

## Demo Showcases

### Leak Investigation Demo
> "Someone leaked our product design on Twitter. We take that image, upload it to InvisID... and it extracts: Employee ID EMP-007. We check our logs and confirm: EMP-007 downloaded this file yesterday at 10:30 AM. Case closed."

### Attack Resilience Demo
> "Watch as I compress this image to 10% JPEG quality, add Gaussian noise... [runs attack] ...our system still extracts the watermark with 87% confidence."

---

## Documentation

- **[FINAL_PLAN.md](./FINAL_PLAN.md)** - Complete implementation plan
- **API Docs** - Available at `/docs` when running the app

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Acknowledgments

- **[invisible-watermark](https://github.com/ShieldMnt/invisible-watermark)** library by ShieldMnt
- **[FastAPI](https://github.com/tiangolo/fastapi)** framework by Sebastián Ramírez
