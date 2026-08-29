# Free deployment

## Backend: Render

1. Rotate any MongoDB password or Groq key that has been pasted into chat, an issue, or another public location.
2. Push this repository to GitHub and create a Render Blueprint from it. Render reads the root `render.yaml` and creates the free FastAPI web service.
3. In the Render service's **Environment** settings, set:

   - `MONGODB_URI`: the rotated MongoDB Atlas connection string
   - `GROQ_API_KEY`: the rotated Groq API key
   - `CORS_ORIGINS`: the final Vercel origin, for example `https://your-project.vercel.app` (no brackets and no trailing slash)

`MONGODB_DATABASE`, `GROQ_MODEL`, `JWT_EXPIRY_MINUTES`, and a generated `JWT_SECRET` are supplied by `render.yaml`. The API start command is `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, and `/health` is used for health checks.

## Frontend: Vercel

1. Import the same GitHub repository into Vercel.
2. Set **Root Directory** to `frontend`; Vercel will detect Vite and run `npm run build`.
3. Set `VITE_API_URL` to the deployed Render API origin, for example `https://loan-data-verification-copilot-api.onrender.com` (no `/api` suffix and no trailing slash).
4. Deploy the frontend, copy its final `https://...vercel.app` URL into Render's `CORS_ORIGINS`, and redeploy the backend.
5. Verify the backend `/health`, then log in through the frontend and exercise upload, validation, AI review, and verified-record flows.

Secrets belong only in Render environment variables and local `backend/.env`. Never place database, JWT, or Groq secrets in any Vercel `VITE_` variable.

## Free-tier behavior

Render free web services sleep after 15 minutes without traffic, so the first API request after inactivity can take about a minute. MongoDB Atlas M0 and Vercel Hobby are suitable for a hackathon/demo workload, but this setup is not production-grade hosting.
