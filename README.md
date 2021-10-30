# Open Weather Map Api by https://openweathermap.org/

## First you need: 
1. Create account https://home.openweathermap.org/users/sign_up
2. Generate your api key https://home.openweathermap.org/api_keys

## Next step: 
1. Choice or make a folder
> $ mkdir openweathermapapi
> $ cd openweathermapapi
2. Clone this project
> $ git clone https://github.com/GOLDLEO/openweathermapapi.git
3. Create a config file `config.py` with next content in current directory 
```python
config = {}
config['API_KEY'] = <your api key>
config['city'] = <you city name>
config['lang'] = <ru> or etc  https://openweathermap.org/current#multi
concig['units] = 'metric'
```
4. Create virtual environment
> $ createvirtual env
5. Activate env
> $ source env/bin/activate
7. Install dependencies
> (env)$ pip install -r requirements.txt
8. Running tests to make sure everything works
> $ python3 openweathermapapi.py runtests

Enjoy:)
