from aiohttp import ClientSession
from .objects import ReturnImage, ToReturnImage, \
									ReturnImageException


__AUTHOR__ = "xaquake"
__API__ = "https://api.api-ninjas.com/v1/imagetotext"

class Client:
	
	def __init__(self, __key):
		self.key = __key
		self.headers = {'X-Api-Key': __key}
	
	@property
	def update_key(self) -> None:
		self.headers['X-Api-Key'] = self.key
	
	async def __response_receiver(self, __image: bytes):
		session = ClientSession()
		async with session.post(__API__, data={'image': __image}, headers=self.headers) as response:
			await session.close()
			return (response.status, await response.json())
	
	async def solving_image(self, __image: bytes) -> [ReturnImage, ReturnImageException]:
		__status_code, __data = await self.__response_receiver(__image)
		if __status_code != 200:
			raise ReturnImageException(__status_code, __data)
		else:
			return ToReturnImage.serialise(__data)
	
	@staticmethod
	def image_to_bytes(__path) -> bytes:
		return open(__path, "rb").read()
