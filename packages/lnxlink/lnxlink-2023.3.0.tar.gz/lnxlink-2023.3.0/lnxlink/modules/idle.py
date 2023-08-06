import subprocess


class Addon():

    def __init__(self, lnxlink):
        self.name = 'Idle'
        self.sensor_type = 'sensor'
        self.icon = 'mdi:timer-sand'
        self.unit = 's'
        self.state_class = 'total_increasing'
        self.device_class = 'duration'

    def getInfo(self):
        stdout = subprocess.run(
            'xprintidle',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).stdout.decode("UTF-8").strip()

        idle_sec = round(float(stdout.strip()) / 1000, 0)

        return idle_sec
