import os
import aiohttp
from xoxxox.shared import Custom

#---------------------------------------------------------------------------

class TtsPrc:

  def __init__(self, config="xoxxox/config_ttsnjv_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    self.keyapi = os.environ["XOXXOX_TTSNJV_KEYAPI"]
    self.keyspk = ""
    self.adrreq = ""
  
  def status(self, config="xoxxox/config_ttsnjv_000", **dicprm):
    diccnf = Custom.update(config, dicprm)
    if self.keyspk != diccnf["keyspk"]:
      self.keyspk = diccnf["keyspk"]
      self.adrreq = f"https://api.nijivoice.com/api/platform/v1/voice-actors/{self.keyspk}/generate-voice"

  async def infere(self, txtreq):
    header = {
      "Content-Type": "application/json",
      "x-api-key": self.keyapi
    }
    datreq = {
      "script": txtreq,
      "speed": "1.0",
      "format": "wav"
    }
    async with aiohttp.ClientSession() as sssweb:
      async with sssweb.post(self.adrreq, headers=header, json=datreq) as datres:
        dicres = await datres.json()
      adrvce = dicres["generatedVoice"]["audioFileUrl"]
      async with sssweb.get(adrvce) as datres:
        datwav = await datres.read()
        return datwav
