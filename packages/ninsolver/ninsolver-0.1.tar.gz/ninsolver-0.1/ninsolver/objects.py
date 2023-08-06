from dataclasses import dataclass


@dataclass(frozen=True)
class ReturnImage:
	
	__slots__ = ('tuple_text', 'bounding_box')
	tuple_text: tuple[str]
	bounding_box: tuple[dict]
	
	@property
	def as_str(self) -> str:
		return ' '.join(self.tuple_text)


class ToReturnImage:
	
	@staticmethod
	def serialise(__json_to: dict) -> ReturnImage:
		__list_text = []
		__list_bounding = []
		for x in __json_to:
			__list_text.append(x['text'])
			__list_bounding.append(x['bounding_box'])
		return ReturnImage(tuple(__list_text), tuple(__list_bounding))


class ReturnImageException(Exception):
	
	def __init__(self, __status_code: int, __json: dict) -> None:
		super().__init__(f"status_code: {__status_code}, error: {__json['error']}")
