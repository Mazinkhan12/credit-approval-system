# Credit Approval Predictor

This turns the model you trained in Colab into a real, working website you
can open in your browser and use.

```
credit-approval-system/
├── backend/
│   ├── app.py              <- the Python server
│   ├── requirements.txt    <- what to install
│   └── models/              <- put your 3 downloaded .joblib files here
└── frontend/
    ├── index.html            <- the form
    ├── style.css
    └── script.js
```

## Setup (do this once)

1. **Install Python**, if you don't already have it: https://www.python.org/downloads/
   During install, tick the box that says **"Add Python to PATH"**.

2. **Copy your 3 files** from Colab into `backend/models/`:
   - `credit_model.joblib`
   - `credit_scaler.joblib`
   - `credit_encoders.joblib`

3. **Open a terminal** in the `backend` folder.
   - On Windows: open the `backend` folder in File Explorer, click the
     address bar, type `cmd`, and press Enter.

4. **Install the required libraries:**
   ```
   pip install -r requirements.txt
   ```

## Run it

Still inside the `backend` folder, run:
```
python app.py
```

You should see:
```
Credit Approval Predictor backend starting...
Open http://127.0.0.1:5000 in your browser.
```

Now open your browser and go to **http://127.0.0.1:5000** — you'll see the
real form, and submitting it calls your actual trained model.

To stop the server, go back to the terminal and press `Ctrl + C`.

## A note on the field labels

The original dataset's column names were anonymized by its source to
protect applicant privacy (see Step 1 of our project). The labels used in
the form (Gender, Age, Debt, etc.) are a commonly-referenced *unofficial*
guess at what each field represents — not confirmed by the dataset itself.
This is fine for learning and demoing, but a real bank would replace these
with actual, verified fields.

## Putting it online (Render, free)

1. Create a free account at https://github.com and https://render.com
   (sign into Render using your GitHub account — it's faster).
2. On GitHub, create a new repository and upload this whole
   `credit-approval-system` folder (drag-and-drop works fine in the
   browser — no command-line git needed, since these files are tiny).
3. On Render: **New → Web Service** → connect your new repository.
4. Set these values:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Click **Create Web Service** and wait a few minutes for the first
   build. Render gives you a live `https://your-app-name.onrender.com`
   link when it's done — that's your real, public website.

Note: on Render's free tier, the site "sleeps" after 15 minutes with no
visitors and takes about a minute to wake back up on the next visit.
That's normal, and fine for a demo/portfolio project.

## Other next steps (optional)

- **Add a login system** so only authorized staff can use it.
- **Log every prediction** to a database for review and auditing.
- **Add human review** for borderline cases, as your original document
  recommended — the model's prediction should assist a decision, not
  replace it outright.
