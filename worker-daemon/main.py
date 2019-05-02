import time
import mongoengine
from datetime import datetime
import simpleaudio as sa

from models import *


mongoengine.connect('bell_server')

while True:
    default = Defaults.objects().first()

    today = CustomSchedule.objects(date=datetime.now().date()).first()
    default_schedule = default.daily_templates[datetime.now().date().weekday()]
    schedule = today if today else default_schedule

    now = datetime.now().time().strftime("%H-%M-%S")
    bell = schedule.times.objects(time=now).first()
    if bell:
        sound_id = bell.sound if bell.sound else default.sound
        filename = Sound.objects(_id=bell.sound).first().sound_filepath
        wav_obj = sa.WaveObject.from_wave_file(filename)
        wav_obj.play()
        time.sleep(1)
