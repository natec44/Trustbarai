TrustBar AI - Streamlit Prototype

Files:
- app.py : Streamlit application prototype. Replace TrustBarAI.png with your logo in the same directory.
- requirements.txt : Python dependencies.
- README contains deployment and embed instructions.

How to run locally:
1. Create a virtualenv and install requirements:
   python -m venv venv
   source venv/bin/activate  # (Windows: venv\Scripts\activate)
   pip install -r requirements.txt
2. Set your OpenAI API key as an environment variable:
   export OPENAI_API_KEY='your_api_key_here'  # Windows: set OPENAI_API_KEY=your_api_key_here
3. Run:
   streamlit run app.py

Deploy to Streamlit Cloud:
1. Create a GitHub repo with these files and your logo image (TrustBarAI.png).
2. Sign in to https://share.streamlit.io (Streamlit Cloud) and connect your GitHub repo.
3. Deploy the app; Streamlit will provide a public URL you can embed in your WordPress site via an iframe.

Embedding in WordPress (Elementor):
1. In the Elementor page editor, add an HTML widget where you want the dashboard.
2. Insert the iframe HTML:
   <iframe src="https://your-streamlit-app-url" width="100%" height="900" style="border:none;"></iframe>
3. Adjust height to fit content. For restricted access, consider protecting the page or using a logged-in only page.

Security & Compliance:
- Do not share API keys publicly.
- Add clear disclaimers in the UI: AI is an assistant and not a substitute for licensed legal advice.
- For production, implement secure authentication, data encryption, and privacy controls.
