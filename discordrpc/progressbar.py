import time
from .exceptions import *


def Progressbar(current:int, duration:int) -> dict:
	if int(current) > int(duration):
		raise ProgressbarError("Current cannot exceed Duration")

	current_time = int(time.time()) - int(current)
	finish_time = current_time + int(duration)

	return {
		"ts_start": current_time, "ts_end": finish_time
	}
