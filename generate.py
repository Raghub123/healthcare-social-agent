import json, random, os, textwrap
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TOPICS = [
 ('Appointment reminders', 'Missed appointments can disrupt clinic operations. A digital reminder workflow helps staff communicate consistently.', 'Ask us how a patient portal can support appointment communication.'),
 ('Patient registration', 'Paper-based registration can create repetitive work. Digital intake can help teams organize patient-provided information.', 'Explore simpler registration workflows for your clinic.'),
 ('Clinic websites', 'A clear clinic website can explain services, locations, working hours and appointment options.', 'Is your clinic website answering patients’ most common questions?'),
 ('Follow-up workflows', 'Structured follow-up workflows can help clinic staff track pending administrative tasks.', 'Talk to us about practical clinic workflow improvements.'),
]

def main():
    out = Path('drafts'); out.mkdir(exist_ok=True)
    date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    idx = int(datetime.now(timezone.utc).strftime('%j')) % len(TOPICS)
    title, body, cta = TOPICS[idx]
    post = f'{title}: a practical opportunity for small clinics.\n\n{body}\n\n{cta}\n\n#DigitalHealth #ClinicManagement #HealthcareTechnology'
    record = {'id':date, 'status':'DRAFT', 'approved':False, 'topic':title, 'platforms':['linkedin','facebook','instagram'], 'post':post, 'image':f'{date}.png', 'created_utc':datetime.now(timezone.utc).isoformat(), 'source':'curated templates; not AI-generated', 'review_notes':'Verify claims, brand and local healthcare advertising rules before approval.'}
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
    print('Created',date,'draft and graphic; NOT published')

if __name__=='__main__':main()
