ATM Greedy Demo

This demo contains a simple greedy algorithm for making change and a Streamlit UI to try it.

Files
- core.py: greedy_change(amount, denominations) implementation
- streamlit_app.py: Streamlit demo
- requirements.txt: minimal dependencies
- Dockerfile: containerizes the demo

Run locally
- pip install -r requirements.txt
- streamlit run streamlit_app.py

Run with Docker:
- Open Docker Desktop and ensure it's running.
- cd algorithm-hus
- docker compose build atm_greedy
- docker compose up -d atm_greedy
- Access the demo at http://localhost:8501
- Code change: update code and run `docker compose restart atm_greedy`
- Logs: `docker compose logs -f atm_greedy --tail 100`

