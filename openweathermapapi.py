import requests
import sys
from pprint import pprint

from exceptions import ApiKeyValueError

from config import config



class OpenWeather:
	def __init__(self, token_api=None, lang='ru', units='metric'):
		""" Initializing an instance of a class OpenWeather. Be sure to enter the API KEY.
		params: self.coord_by_city(self, city=None)
		"""
		if token_api is None:
			raise ApiKeyValueError('To work with the service, you need to specify the api key. Loot here: https://www.openweathermapapi.com')		
		self.token_api = token_api
		self.lang = lang
		self.units = units
		self.base_url = 'http://api.openweathermap.org/data/2.5/'

	def current_weather_by_city(self, city=None):
		""" This is function return all data about weather in your city. 
		params: self.coord_by_city(self, city=None)
		"""
		data_json = {'status':'','message':''} # создаем пустой словарь для вывода данных
		if city is None:
			data_json['status'] = 400
			data_json['message'] = 'Пустое значение параметра город. Введите свой город.'
		else:
			url = self.base_url + f'weather?q={city}&appid={self.token_api}&lang={self.lang}&units={self.units}'
			response = requests.get(url)
			if response.status_code == 401: # invalid api key 
				data_json['status'] = response.status_code
				data_json['message'] = response.json()['message'] + "Некорретный ключ API"
			elif response.status_code == 404: # bad query request
				data_json['status'] = response.status_code
				data_json['message'] = response.json()['message'] + "Проверьте правильность названия вашего города"
			elif response.status_code == 200: # status ok 
				data_json['status'] = response.status_code
				data_json['data'] = response.json()

		return data_json


	def coord_by_city(self, city=None):
		""" This is function return coordinates by your city. It is need for other methods because api service work just with latitude and longitude. 
		params: self.coord_by_city(self, city=None)
		"""
		data_json = {}
		if city is None:
			data_json['status'] = 400
			data_json['message'] = 'Пустое значение параметра город. Введите свой город.'
		else:
			url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={self.token_api}'
			response = requests.get(url)
			
			try:
				data_json['data'] = tuple([response.json()[0]['lat'],response.json()[0]['lon']])
				data_json['status'] = 200
			except Exception as err:
				print(err)
				data_json['status'] = 404
				data_json['message'] = err

		return data_json




	def air_pollution(self, city=None):
		""" This is function show national danger alerts in your country or city 
		params: self.alerts(self, city=None)
		"""
		data_json = {}
		if city is None:
			data_json['status'] = 400
			data_json['message'] = 'Пустое значение параметра город. Введите свой город.'
		else:
			try:
				lon, lat = tuple(self.coord_by_city(city)['data'])
			except Exception as err:
				data_json['status'] = 400
				data_json['message'] = err
				return data_json

			url = self.base_url + f'air_pollution?lat={lat}&lon={lon}&appid={self.token_api}&lang={self.lang}'
			response = requests.get(url)
			if response.status_code == 200:
				data_json['status'] = 200
				data_json['data'] = response.json()
			elif response.status_code == 400:
				data_json['status'] = response.status_code
		return data_json


	def alerts(self, city=None):
		""" This is fucntion show national danger alerts in your country or city 
		params: alerts(self, city=None)
		"""
		data_json = {}
		if city is None:
			data_json['status'] = 404
			data_json['message'] = 'Пустое значение для параметра город. Введите название своего города.'
		else:
			lat, lon = tuple(self.coord_by_city(city)['data'])
			url = self.base_url + f'onecall?appid={self.token_api}&lat={lat}&lon={lon}&units={self.units}&exclude=current,daily,minutely,hourly'
			response = requests.get(url)
			try:
				data_json['status'] = 200
				data_json['data'] = response.json()['alerts']
			except KeyError:
				data_json['message'] = 'Нет опасных предупреждений.'
		return data_json


	


def run_test():
	owm_conn = OpenWeather(token_api=config['API_KEY'], lang=config['lang'], units=config['units'])
	city = config['city']
	pprint(owm_conn.air_pollution(city))
	pprint(owm_conn.current_weather_by_city(city))

	assert owm_conn.current_weather_by_city(city)['status'] == 200
	assert owm_conn.air_pollution(city)['status'] == 200
	assert owm_conn.coord_by_city(city)['status'] == 200
	assert owm_conn.alerts(city)['status'] == 200 


if __name__ == '__main__':
	if sys.argv[1] == 'runtests':
		print('Запускаем модуль', sys.argv[0])
		print('Запускаем тесты')
		run_test()
		print('Тест окончен.')
	if sys.argv[1] == '--help' or sys.argv[1] == '-H':
		print('class OpenWeather')
		print('\t__init__(self, token_api="3d68c5s9e1209asdab832ca3a3517d2b0", lang="ru", units="metric"')
		print('All methods: ')
		for method in reversed(dir(OpenWeather)):
			try:
				if '__' not in method:
					print('\tdef', method)
					print('\t\tDescription: ', end='')
					print('',eval('OpenWeather.' + method + '.__doc__'))
					print()
			except:
				pass
		print('Example how it works:')

		string_example = """
		from pprint import pprint

		openweather_connect = OpenWeather(token_api="3d68c5s9e1209asdab832ca3a3517d2b0", lang="en", units="metric")
		my_city = 'Paris'
		if openweather_connect.current_weather_by_city(my_city)['status'] == 200:
			pprint(openweather_connect.current_weather_by_city(my_city))
			pprint(openweather_connect.air_pollution(my_city))


			OR  

		data = openweather_connect.current_weather_by_city('Париж')['data']
		pprint(data)"""
		print(string_example)




