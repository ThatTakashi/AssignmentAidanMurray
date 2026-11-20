# Testing the Clinic API with Postman

This guide walks through testing every REST endpoint using Postman.

## 1. Setup

1. Start the Django backend:
   ```bash
   python manage.py runserver
   ```
   The API is available at `http://localhost:8000/api/`
   (on Render, use `https://<your-api>.onrender.com/api/` instead).

2. In Postman, create a new Collection named **Clinic API**.

3. Set a collection variable for convenience:
   - Click the collection → **Variables** tab
   - Add `base_url` = `http://localhost:8000/api`
   - You can then use `{{base_url}}` in every request URL.

## 2. Authentication (JWT)

The API uses JWT tokens. You must log in first and attach the returned
`access` token to every protected request.

### Step 1 — Register a patient (optional)

- **Method:** `POST`
- **URL:** `{{base_url}}/register/`
- **Body** → `raw` → `JSON`:
  ```json
  {
    "username": "testpatient",
    "email": "patient@test.com",
    "password": "testpass123"
  }
  ```
- **Expected:** `201 Created` → `{"detail": "Registration successful."}`

### Step 2 — Log in to get tokens

- **Method:** `POST`
- **URL:** `{{base_url}}/token/`
- **Body** → `raw` → `JSON`:
  ```json
  {
    "username": "testpatient",
    "password": "testpass123"
  }
  ```
- **Expected:** `200 OK` with:
  ```json
  {
    "refresh": "<long token>",
    "access": "<long token>"
  }
  ```

### Step 3 — Attach the token to requests

Copy the `access` token value, then either:

- **Option A (recommended):** In Postman, go to the **Authorization** tab of each
  request (or set it at the collection level under **Authorization** →
  Type: `Bearer Token` → paste the token). Every request in the collection then
  sends `Authorization: Bearer <token>` automatically.
- **Option B:** Manually add a header:
  `Authorization: Bearer <paste access token here>`

> Tokens expire after 1 hour. To get a new one without re-entering the
> password, `POST` to `{{base_url}}/token/refresh/` with
> `{"refresh": "<refresh token>"}`.

### Step 4 — Check who you are

- **Method:** `GET`
- **URL:** `{{base_url}}/me/`
- **Expected:** `200 OK`
  ```json
  {"id": 2, "username": "testpatient", "email": "patient@test.com", "is_staff": false}
  ```

## 3. Doctors

| Method | URL | Who | Body |
|---|---|---|---|
| GET | `{{base_url}}/doctors/` | any logged-in user | — |
| GET | `{{base_url}}/doctors/1/` | any logged-in user | — |
| POST | `{{base_url}}/doctors/` | **admin only** | JSON below |
| PATCH | `{{base_url}}/doctors/1/` | **admin only** | partial JSON |
| DELETE | `{{base_url}}/doctors/1/` | **admin only** | — |

**POST body example:**
```json
{
  "name": "Smith",
  "speciality": "General Practice",
  "email": "smith@clinic.com",
  "phone": "0211234567"
}
```

**Permission test:** log in as a normal patient and `POST` to `/doctors/` —
you should get `403 Forbidden`.

## 4. Appointment Slots

| Method | URL | Who | Notes |
|---|---|---|---|
| GET | `{{base_url}}/slots/` | any logged-in user | list all slots |
| GET | `{{base_url}}/slots/?doctor=1&is_available=true` | any logged-in user | filter by doctor / availability |
| POST | `{{base_url}}/slots/` | **admin only** | create a slot |
| PATCH/DELETE | `{{base_url}}/slots/1/` | **admin only** | update / delete |

**POST body example:**
```json
{
  "doctor": 1,
  "date": "2026-12-01",
  "start_time": "09:00:00",
  "end_time": "09:30:00"
}
```

> `doctor` is the doctor's **ID** (get it from `GET /doctors/`).
> Creating a duplicate `(doctor, date, start_time)` returns `400`.

## 5. Appointments

| Method | URL | Who | Notes |
|---|---|---|---|
| GET | `{{base_url}}/appointments/` | patient sees **own only**; admin sees **all** | |
| POST | `{{base_url}}/appointments/` | any logged-in user | book a slot |
| PATCH | `{{base_url}}/appointments/1/` | owner or admin | update `status` / `notes` |
| DELETE | `{{base_url}}/appointments/1/` | **admin only** | |

**Book an appointment (POST body):**
```json
{ "slot": 1 }
```
- `slot` is the slot **ID**.
- The patient is set automatically from your login — do not send `patient`.
- Expected: `201 Created`. Booking the same slot twice returns `400`
  ("The selected slot is already booked.").

**Update / cancel (PATCH body examples):**
```json
{ "status": "cancelled" }
```
```json
{ "notes": "Please call before appointment" }
```
Cancelling frees the slot (`is_available` becomes `true` again).

## 6. Testing checklist

- [ ] Register a new patient → `201`
- [ ] Login → receive `access` + `refresh` tokens
- [ ] `GET /me/` without a token → `401 Unauthorized`
- [ ] Patient `GET /doctors/`, `/slots/`, `/appointments/` → `200`
- [ ] Patient `POST /doctors/` → `403 Forbidden`
- [ ] Patient books a slot → `201`, appears in `GET /appointments/`
- [ ] Patient tries booking the same slot again → `400`
- [ ] Patient `PATCH` own appointment status/notes → `200`
- [ ] Patient `DELETE /appointments/1/` → `403 Forbidden`
- [ ] Login as **admin** (`is_staff=true`) → sees **all** appointments,
      can create/edit/delete doctors and slots
- [ ] `POST /token/refresh/` with the refresh token → new access token

## 7. Admin account

To test admin endpoints you need a staff user. Locally:

```bash
python manage.py createsuperuser
```

Then log in via `POST /token/` with those credentials — the returned user
will have `"is_staff": true`.
