from .base_output_device import BaseOutputDevice
from ..models.audio_encoding import AudioEncoding

class Telephone(BaseOutputDevice):

    def __init__(self):
        super().__init__(sampling_rate=8000, audio_encoding=AudioEncoding.MULAW)

    async def send_async(self, chunk):
        raise NotImplemented