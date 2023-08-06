import setuptools

big_descr = """
__ninsolver python library for solving captchas__

---

__python version 3.5+__

to install with pip:

```pip install ninsolver```

requirements:

```aiohttp```

code example:

```
from asyncio import run, gather
import ninsolver

async def async_append(client, image, to_append, num):
	res = await client.solving_image(client.image_to_bytes(image))
	to_append.append(res)
	print(f"{num} - solved")

async def main():
	client = ninsolver.Client("YOUR API KEY")
	results = []
	await gather(*[async_append(client, f"{i}.jpg", results, i) for i in range(1, 7)])
	for x in results:
		print(x.as_str)

run(main())
```

__links:__

- [telegram](https://t.me/xarlchat)

- [github](https://github.com/xaquake)

p.s. visit my github, there are also other codes there
"""

setuptools.setup(name='ninsolver',
      description='library for solving captchas using https://api.api-ninjas.com/v1',
      version = "0.3",
      packages=["ninsolver"],
      long_description = big_descr,
      long_description_content_type='text/markdown',
      author_email='bonnita1900432@gmail.com')
