# Village des Benjamins

Reservation management system for the ASBL Village des Benjamins.

## Tech Stack

- **Backend**: Django 6.0 with Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Vue.js
- **Package Manager**: uv (Python), npm (JavaScript)
- **Development Environment**: Nix with devenv
- **Email**: SendGrid (production), Mailpit (development)
- **Storage**: AWS S3 (production), MinIO (development)

## Local Development Setup

### Prerequisites

- [Nix](https://nixos.org/download.html) with flakes enabled
- [direnv](https://direnv.net/) (recommended)

### Quick Start

1. **Enter the development environment**:
   ```bash
   # If using direnv (recommended)
   direnv allow

   # Or manually enter the nix shell
   nix develop
   ```

   This automatically sets up:
   - Python 3.13 with uv
   - Node.js with npm
   - PostgreSQL (database: `vdb`, user: `vdb`)
   - MinIO (S3-compatible storage on port 9000)
   - Mailpit (email testing on ports 1025/8025)
   - All necessary environment variables

2. **Start background services**:
   ```bash
   devenv up
   ```

   This starts PostgreSQL, MinIO, and Mailpit in the background.

3. **Run database migrations** (in a new terminal):
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Frontend: http://localhost:8000
   - Admin panel: http://localhost:8000/admin
   - Mailpit (emails): http://localhost:8025
   - MinIO console: http://localhost:9001 (minioadmin/minioadmin)

### Development Services

#### PostgreSQL
- Automatically started by devenv
- Database: `vdb`
- User: `vdb` (superuser)
- Connection via Unix socket

#### Email Testing (Mailpit)
All emails sent during local development are captured by Mailpit.
- Web interface: http://localhost:8025
- SMTP port: 1025
- View all sent emails without actually sending them

#### Storage Testing (MinIO)
Local S3-compatible object storage for file uploads.
- Console: http://localhost:9001
- API: http://localhost:9000
- Credentials: minioadmin/minioadmin
- Bucket: `village-des-benjamins` (auto-created)

### Common Commands

```bash
# Install new Python package
uv add <package-name>

# Install dev dependency
uv add --dev <package-name>

# Run Django management command
python manage.py <command>

# Run tests
python manage.py test

# Format code
treefmt

# Start all background services
devenv up

# Stop all services
# Press Ctrl+C in the devenv up terminal

# Update flake dependencies
nix flake update
```

### Project Structure

```
village_des_benjamins/
├── frontend/               # Vue.js frontend
├── holiday/               # Holiday/vacation management
├── members/               # User and child management
├── parent_messages/       # Parent communication
├── section/               # Section/group management
├── site_content/          # CMS content
├── village_des_benjamins/ # Django project settings
├── flake.nix              # Nix flake with devenv config
├── pyproject.toml         # Python dependencies (uv)
└── manage.py              # Django management script
```

## Environment Variables

All development environment variables are configured in `flake.nix` under the `env` section. You can override them by creating a `.env` file in the project root.

Key variables:
- `DATABASE_URL` - PostgreSQL connection (auto-configured)
- `DEBUG` - Django debug mode (true in dev)
- `EMAIL_HOST` / `EMAIL_PORT` - Mailpit configuration
- `AWS_S3_ENDPOINT_URL` - MinIO endpoint
- `AWS_STORAGE_BUCKET_NAME` - S3 bucket name

## Production Deployment

Production uses:
- PostgreSQL database
- SendGrid for email delivery
- AWS S3 for file storage
- Sentry for error tracking

Required environment variables:
- `SECRET_KEY`
- `DATABASE_URL`
- `SENDGRID_API_KEY`
- `MAIL_FROM_ADDRESS`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `SENTRY_DSN`
- `DEBUG=false`
- `SSL=true`

## Nix Development Environment

This project uses [devenv](https://devenv.sh/) for reproducible development environments. The configuration in `flake.nix` includes:

- Python environment with Poetry/uv
- Node.js environment with npm
- PostgreSQL database service
- MinIO S3-compatible storage
- Mailpit email testing server
- Pre-commit hooks for code quality
- Code formatters (black, prettier, etc.)

To update the development environment configuration, edit `flake.nix` and run:
```bash
nix flake lock --update-input devenv
```
