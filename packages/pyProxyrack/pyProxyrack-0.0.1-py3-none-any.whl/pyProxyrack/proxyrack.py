import requests

from .exceptions import *

class Proxyrack:
	def __init__(self, API_BASE_URL = "https://peer.proxyrack.com", API_PREFIX = "/api", API_VERSION = "") -> None:
		"""Initialises Proxyrack class. """
		self.API_URL = API_BASE_URL + API_PREFIX + API_VERSION

		self.remove_all_headers()
		self.add_default_headers({
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
			"Origin": "https://peer.proxyrack.com",
			"Referrer": "https://peer.proxyrack.com",
			"Content-Type": "application/json",
			"Accept": "application/json",
		})

		self.remove_proxy()
		self.logout()

	def remove_all_headers(self) -> bool:
		"""Removes all default headers for future requests. """
		self.__headers = {}

	def add_default_headers(self, headers: dict = {}) -> bool:
		"""Adds default headers for future requests. Could be used to set user-agent for example. """
		self.__headers = {
			**self.__headers, **headers
		}

		return True

	def __return_response(self, response) -> dict:
		"""Return an easy to navigate dict. """
		result = {}

		result["json"] = None

		result["success"] = bool(response.ok)

		try:
			# Try this line, because you might not get a response everytime
			result["json"] = response.json()
		except:
			pass

		result["response"] = response

		return result

	def logout(self) -> bool:
		"""Sets API Key to None. """
		return self.set_api_key(None)

	def __make_request(self, req_type: str, endpoint: str, headers: dict = {}, *args, **kwargs):
		"""Helper function to make requests. """

		return requests.request(req_type, f'{self.API_URL}{endpoint}', proxies = self.proxy_conf, headers = {
            **self.__headers, **headers, **({
                "Api-Key": f"{self.api_key}",
            } if self.is_logged_in() else {}),
        }, *args, **kwargs)

	def set_proxy(self, proxy_str: str = None, protocol: str = "socks5") -> bool:
		"""Sets the proxy for future API requests."""

		if proxy_str is None:
			self.proxy_conf = None
			return True

		proxy = proxy_str.split(":")

		if len(proxy) > 2:
			ip, port, username, password = proxy

			self.proxy_conf = {
				"http": f"{protocol}://{username}:{password}@{ip}:{port}",
				"https": f"{protocol}://{username}:{password}@{ip}:{port}",
			}
		else:
			ip, port = proxy

			self.proxy_conf = {
				"http": f"{protocol}://{ip}:{port}",
				"https": f"{protocol}://{ip}:{port}",
			}

		return True

	def set_socks5_proxy(self, proxy_str: str = None) -> bool:
		"""Sets SOCKS5 proxy for future API requests. """
		return self.set_proxy(proxy_str, "socks5")

	def set_http_proxy(self, proxy_str: str = None) -> bool:
		"""Sets HTTP proxy for future API requests. """
		return self.set_proxy(proxy_str, "http")

	def set_https_proxy(self, proxy_str: str = None) -> bool:
		"""Sets HTTPS proxy for future API requests. """
		return self.set_proxy(proxy_str, "https")

	def remove_proxy(self) -> bool:
		"""Removes the proxy for future API requests. """
		return self.set_proxy(None)

	def __handle_not_logged_in(self) -> None:
		if not self.is_logged_in():
			raise NotLoggedInError

	def is_logged_in(self) -> bool:
		"""Returns if we're logged in or not. """
		return self.api_key is not None

	def set_api_key(self, key: str = None) -> bool:
		"""Sets the API Key for future requests. """
		self.api_key = key
		return True

	def get_device_bandwidth_usage(self, device_id: str = None, date_start: str = None, date_end: str = None) -> dict:
		"""Returns bandwidth information. 
		@param date_start is a string in Y-m-d format
		@param date_end is a string in Y-m-d format
			(If dates not specified - data for last 7 days will be returned.)
		@param device_id is a string ID of device for bandwidth review.
			(If device_id is None, data contains list of all the devices.)
		"""

		self.__handle_not_logged_in()

		response = self.__make_request("POST", "/bandwidth", params = {
			**({"device_id": device_id} if device_id else {}),
			**({"date_start": date_start} if date_start else {}),
			**({"date_end": date_end} if date_end else {}),
		})

		return self.__return_response(response)

	def add_device(self, device_id: str, device_name: str) -> dict:
		"""Adds/links a device to the account. """

		self.__handle_not_logged_in()

		response = self.__make_request("POST", "/device/add", params = {
			"device_id": device_id,
			"device_name": device_name,
		})

		return self.__return_response(response)
	
	def delete_device(self, device_id: str) -> dict:
		"""Deletes a device from the account. """

		self.__handle_not_logged_in()

		response = self.__make_request("POST", "/device/delete", params = {
			"device_id": device_id,
		})

		return self.__return_response(response)

	def __repr__(self):
		"""Represents the Proxyrack object. """
		return f"<Proxyrack object at {hex(id(self))}>"
