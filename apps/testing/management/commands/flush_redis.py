from django.core.management.base import BaseCommand
from decouple import config
from django.utils import termcolors
import redis
import sys

class Command(BaseCommand):
    help = "Completely clears the Redis database"
    
    def handle(self, *args, **kwargs):        
        try:
            r = redis.Redis(
                host=config('REDIS_HOST'),
                port=config('REDIS_PORT'),
                db=config('REDIS_DB'),
                password=config('REDIS_PASSWORD'),
                socket_timeout=5
            )
            
            r.ping()
            r.flushdb()
            self.stdout.write(termcolors.make_style(fg="green")('✓ Redis flushed'))
             
        except redis.AuthenticationError:
            self.stdout.write(termcolors.make_style(fg="red")('✘ Redis password is incorrect'))
            sys.exit(1)
        except redis.ConnectionError:
            self.stdout.write(termcolors.make_style(fg="red")('✘ Could not connect to Redis server'))
            sys.exit(1)
        except Exception as e:
            self.stdout.write(termcolors.make_style(fg="red")(f'✘ Unknown error: {str(e)}'))
            sys.exit(1)