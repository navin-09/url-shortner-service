# URL Shortener Service

⚙️ **Setup**

- Create a `.env` file in the project root with at least:
  ```
  DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/url_shortener
  REDIS_URL=redis://redis:6379/0
  BASE_URL=http://localhost:8080
  SHORT_CODE_LENGTH=8
  ```

🧪 **Build & Run**

- Build images and start containers:

  ```
  docker compose up --build
  ```

- In another terminal, check health:
  ```
  curl http://localhost:8080/health
  # -> {"status":"ok"}
  ```

🔍 **Test API (curl examples)**

1️⃣ **Create short URL**

```
curl -X POST http://localhost:8080/api/v1/urls \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://openai.com"}'

# -> {"short_code":"Ab12CdEf","short_url":"http://localhost:8080/Ab12CdEf"}
```

2️⃣ **Resolve / redirect**

```
curl http://localhost:8080/Ab12CdEf
# -> {"redirect_to":"https://openai.com"}
```

3️⃣ **Inspect Redis cache**

```
docker compose exec redis redis-cli KEYS "*"

# Example:
# "url:Ab12CdEf"
# "clicks:Ab12CdEf"
```

4️⃣ **Inspect Postgres records**

```
docker compose exec db psql -U postgres -d url_shortener \
  -c "SELECT short_code, original_url, click_count FROM url_mapping;"
```
