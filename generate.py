import json, os, textwrap, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import urllib.error

TOPICS = [
 ('Appointment reminders', 'Missed appointments can disrupt clinic operations. A digital reminder workflow helps staff communicate consistently.', 'Ask us how a patient portal can support appointment communication.'),
 ('Patient registration', 'Paper-based registration can create repetitive work. Digital intake can help teams organize patient-provided information.', 'Explore simpler registration workflows for your clinic.'),
 ('Clinic websites', 'A clear clinic website can explain services, locations, working hours and appointment options.', 'Is your clinic website answering patients’ most common questions?'),
 ('Follow-up workflows', 'Structured follow-up workflows can help clinic staff track pending administrative tasks.', 'Talk to us about practical clinic workflow improvements.'),
 ('Hospital ERP', 'Small hospitals often coordinate billing, registration, inventory and clinical administration across multiple workflows.', 'Explore how integrated workflows might simplify your operations.'),
 ('Revenue cycle management', 'Clear billing workflows and careful reconciliation can help teams identify administrative gaps.', 'Learn more about practical RCM workflow improvements.'),
]

def ai_draft(topic, context):
    key = os.getenv('GEMINI_API_KEY', '').strip()
    if not key:
        raise RuntimeError('GEMINI_API_KEY missing')
    model = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    prompt = f'''Create ONE original B2B social media marketing draft for an Indian healthcare technology startup.
Topic: {topic}. Background: {context}
Audience: owners and administrators of clinics and hospitals under 50 beds.
Services may include clinic websites, appointment systems, hospital ERP and RCM. Do not claim a feature is launched, proven, or available unless provided as fact.
No patient information, medical advice, fabricated numbers, testimonials, guarantees or exaggerated outcomes. Do not imply regulatory certification.
Return ONLY a valid JSON object with string keys: title (max 55 characters), post (90-160 words including a modest call to action and 2-4 relevant hashtags). No markdown code fences.'''
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
    payload = json.dumps({'contents':[{'parts':[{'text':prompt}]}], 'generationConfig':{'temperature':0.65,'responseMimeType':'application/json'}}).encode()
    request = urllib.request.Request(url, data=payload, headers={'Content-Type':'application/json','x-goog-api-key':key}, method='POST')
    with urllib.request.urlopen(request, timeout=35) as response:
        result = json.load(response)
    raw = result['candidates'][0]['content']['parts'][0]['text']
    obj = json.loads(raw)
    title, post = obj['title'].strip(), obj['post'].strip()
    if not title or not post or len(title)>70 or len(post)>2000:
        raise ValueError('Invalid model output')
    return title, post

def main():
    out = Path('drafts'); out.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc)
    date = now.strftime('%Y-%m-%d')
    title, body, cta = TOPICS[int(now.strftime('%j')) % len(TOPICS)]
    post = f'{title}: a practical opportunity for small clinics.\n\n{body}\n\n{cta}\n\n#DigitalHealth #ClinicManagement #HealthcareTechnology'
    source = 'curated templates; not AI-generated'
    try:
        title, post = ai_draft(title, body)
        source = 'Gemini AI-generated; human review required'
    except Exception as exc:
        if isinstance(e, urllib.error.HTTPError):
           print(f"Gemini HTTP error: {e.code}")
        else:
           print(f"Gemini error: {type(e).__name__}")

    record = {
        'id':date, 'status':'DRAFT', 'approved':False, 'topic':title,
        'platforms':['linkedin','facebook','instagram'], 'post':post,
        'image':f'{date}.png', 'created_utc':now.isoformat(), 'source':source,
        'review_notes':'Review claims, service availability, brand, and applicable healthcare advertising rules before approval.'
    }
    (out/f'{date}.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    img = Image.new('RGB',(1080,1080),'#102a43'); d = ImageDraw.Draw(img)
    fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    big=ImageFont.truetype(fontpath,65); small=ImageFont.truetype(fontpath,34)
    d.rounded_rectangle((65,75,1015,1005),radius=45,fill='#173d5c')
    d.text((115,150),'HEALTHCARE DIGITAL SOLUTIONS',font=small,fill='#65e2c2')
    y=340
    for line in textwrap.wrap(title,width=21):
        d.text((115,y),line,font=big,fill='white'); y+=90
    d.text((115,860),'Better workflows. Clearer communication.',font=small,fill='#cde5ee')
    img.save(out/f'{date}.png')
    print('Created',date,'draft and graphic; source:',source,'; NOT published')

if __name__=='__main__': main()
