import os
from google import genai
from tracker.models import FistulaCase
from mpdsr.models import MPDSREvent


def generate_newsletter_narrative(month, year):
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return "Error: GEMINI_API_KEY not configured in environment variables."

    total_deaths = MPDSREvent.objects.count()
    pending_actions = MPDSREvent.objects.filter(action_status='PENDING').count()
    fistula_surgeries = FistulaCase.objects.filter(referral_status='OPERATED').count()

    prompt = f"""
    Write a 3-paragraph policy advocacy newsletter for {month}/{year}.
    Highlight the data-to-action gap based on:
    - Total MPDSR Deaths Reported: {total_deaths}
    - Pending Corrective Actions: {pending_actions}
    - Successful Fistula Surgeries: {fistula_surgeries}
    Tone: professional, action-oriented, aimed at health system stakeholders.
    """

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        return response.text
    except Exception as e:
        return f"Error generating narrative: {str(e)}"
