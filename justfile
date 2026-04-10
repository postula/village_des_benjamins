default: list

list:
    @just --list

e2e-user-email := "e2e@test.local"
e2e-user-password := "e2e-password"

e2e-env := "SECRET_KEY=e2e-test-key DATABASE_URL=postgres://vdb@localhost:5433/vdb DEBUG=true ALLOWED_HOSTS=localhost,127.0.0.1 AWS_ACCESS_KEY_ID=minioadmin AWS_SECRET_ACCESS_KEY=minioadmin AWS_S3_MINIO=true AWS_STORAGE_BUCKET_NAME=village-des-benjamins AWS_S3_ENDPOINT_URL=http://127.0.0.1:9100 AWS_S3_REGION_NAME=us-east-1 AWS_LOCATION=website_uploads/ SMTP_HOST=localhost SMTP_PORT=1026 SMTP_USE_TLS=false MAIL_FROM_ADDRESS=noreply@test.local"

# ── General ──────────────────────────────────────────────────────────────────

migrate:
    uv run python manage.py migrate

build-frontend:
    npm run build

serve:
    uv run python manage.py runserver

# ── E2E ───────────────────────────────────────────────────────────────────────

e2e-up:
    docker compose -f docker-compose.e2e.yml up -d --wait
    docker compose -f docker-compose.e2e.yml run --rm minio-init

e2e-down:
    docker compose -f docker-compose.e2e.yml down -v

create-e2e-user:
    #!/usr/bin/env bash
    set -euo pipefail
    env {{ e2e-env }} uv run python manage.py shell -c "
    from django.contrib.auth import get_user_model
    from members.models import Child
    from holiday.models import Holiday
    from datetime import date, timedelta

    User = get_user_model()
    user, created = User.objects.get_or_create(email='{{ e2e-user-email }}')
    user.set_password('{{ e2e-user-password }}')
    user.first_name = 'E2E'
    user.last_name = 'Testeur'
    user.is_staff = True
    user.save()
    print('created' if created else 'updated', '{{ e2e-user-email }}')

    # One child per section age range
    today = date.today()
    children = [
        ('Léa',   'Testeur', 'female', date(today.year - 3, 6, 15)),
        ('Hugo',  'Testeur', 'male',   date(today.year - 5, 3, 10)),
        ('Emma',  'Testeur', 'female', date(today.year - 8, 9, 20)),
        ('Lucas', 'Testeur', 'male',   date(today.year - 11, 1, 5)),
    ]
    for first, last, gender, birth in children:
        child, c = Child.objects.get_or_create(
            first_name=first, last_name=last, parent=user,
            defaults={'gender': gender, 'birth_date': birth, 'status': 'registered'},
        )
        if c:
            print(f'  created child {first} ({birth})')

    # Ensure at least one holiday has registration open
    h = Holiday.objects.order_by('-start_date').first()
    if h and not h.registration_open:
        h.registration_open = True
        h.save()
        print(f'  opened registration for {h.name}')
    "

e2e-seed:
    PGPASSWORD="" psql -h localhost -p 5433 -U vdb vdb < e2e-seed.sql

e2e-setup: e2e-up
    env {{ e2e-env }} uv run python manage.py migrate
    just e2e-seed
    npm run build
    just create-e2e-user

e2e-test *ARGS:
    E2E_USER_EMAIL={{ e2e-user-email }} E2E_USER_PASSWORD={{ e2e-user-password }} npx playwright test {{ ARGS }}

e2e *ARGS:
    #!/usr/bin/env bash
    set -euo pipefail

    just e2e-setup

    env {{ e2e-env }} uv run python manage.py runserver &
    SERVER_PID=$!
    trap "kill $SERVER_PID 2>/dev/null; just e2e-down" EXIT

    until curl -sf http://localhost:8000/api/health/ > /dev/null 2>&1; do sleep 1; done

    E2E_USER_EMAIL={{ e2e-user-email }} E2E_USER_PASSWORD={{ e2e-user-password }} npx playwright test {{ ARGS }}
