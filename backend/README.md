## Structure
```
.
├── Dockerfile (API service image)
├── gunicorn.conf.py (Gunicorn Config)
├── app (Main)
│   ├── database.py (DB)
│   ├── exceptions.py (self-define exceptions)
│   ├── log_config.py
│   ├── main.py
│   ├── assets (save download files)
│   ├── forms
│   │   └── login.py
│   ├── logger (save log files)
│   ├── models (ORM models)
│   │   ├── account.py
│   │   ├── login_hist.py
│   │   ├── team.py
│   │   ├── time.py
│   │   └── vote.py
│   ├── routers (API routing)
│   │   ├── .env
│   │   ├── db.py
│   │   ├── docs.py
│   │   ├── login.py
│   │   ├── teams.py
│   │   ├── time.py
│   │   ├── users.py
│   │   └── vote.py
│   ├── schema (Data Format Encapsulation，資料格式封裝)
│   │   ├── common.py
│   │   ├── team.py
│   │   ├── time.py
│   │   ├── users.py
│   │   └── vote.py
│   ├── services (DB data access，DB 資料存取)
│   │   ├── teams.py
│   │   ├── time.py
│   │   ├── users.py
│   │   └── vote.py
│   └── static (靜態檔案)
│       ├── css
│       │   └── swagger-ui.css
│       ├── images
│       │   └── my-logo.png
│       └── js
│           ├── redoc.standalone.js
│           └── swagger-ui-bundle.js
└── requirements.txt
```