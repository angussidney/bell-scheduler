import mongoengine
import time
from datetime import datetime
import simpleaudio as sa

from models import *

mongoengine.connect('bell_server')

while True:
    default = Defaults.objects().first()

    now = datetime.now()
    any_today = CustomSchedule.objects(date=now.date())
    today = CustomSchedule.objects(date=now.date(), bells__time=now.strftime("%H:%M")).first()
    default_schedule = Template.objects(id=default.daily_templates[now.weekday()],
                                        bells__time=now.strftime("%H:%M")).first()
    schedule = today if any_today else default_schedule

    if schedule:
        for bell in schedule.bells:
            if bell.time == now.strftime("%H:%M"):
                sound_id = bell.sound if bell.sound else default.sound
                filename = Sound.objects(id=sound_id).first().filepath
                wav_obj = sa.WaveObject.from_wave_file(filename)
                wav_obj.play()
                time.sleep(60)
                break
