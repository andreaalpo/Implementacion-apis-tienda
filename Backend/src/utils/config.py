from decouple import config

class Settings:
   SECREET_KEY = config('SECRET_KEY')


class DevelopmentSettings(Settings):
    DEBUG = True

config = {
    'development': DevelopmentSettings,
}