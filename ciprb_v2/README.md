# CIPRB M&E Dashboard

Django-based M&E dashboard for CIPRB/PHD/Bondhu UNFPA-funded MISP programme.

## Features
- KoboToolbox webhook ingestion (Fistula, MPDSR, Baseline)
- Real-time dashboard with Chart.js
- HTMX-powered action status updates
- AI newsletter generation (Gemini)
- PDF and PPT export
- Bilingual (English/Bangla)

## Deployment on Render

### Required Environment Variables (set in Render dashboard)
| Variable | Value |
|---|---|
| `DATABASE_URL` | Your Supabase PostgreSQL connection string |
| `SECRET_KEY` | A long random string (generate at djecrety.ir) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `ciprb-mne-dashboard.onrender.com` |
| `KOBO_WEBHOOK_SECRET` | Your KoboToolbox webhook secret |
| `GEMINI_API_KEY` | Your Google Gemini API key |
| `DJANGO_SUPERUSER_USERNAME` | Admin username |
| `DJANGO_SUPERUSER_EMAIL` | Admin email |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password |

### Render Build & Start Command
```
python manage.py migrate && python manage.py createsuperuser --noinput || true && python manage.py collectstatic --noinput && gunicorn ciprb.wsgi --bind 0.0.0.0:$PORT
```

## Local Development
```bash
pip install -r requirements.txt
export DATABASE_URL=sqlite:///db.sqlite3
export DEBUG=True
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## KoboToolbox Webhook Setup
Point your KoboToolbox forms to:
`https://your-domain.onrender.com/api/kobo/ingest/`

Set header: `X-Kobo-Webhook-Secret: <your KOBO_WEBHOOK_SECRET value>`
