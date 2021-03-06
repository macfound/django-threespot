import subprocess

from django.core.management.base import BaseCommand

from threespot.documentation import app_settings

class Command(BaseCommand):
    
    """
    This Django management command allows you to publish the sphinx 
    documentation for the project. It is run thusly:
        
        $>./manage.py build_docs
    
    By default, it will search for docs in a folder call 'docs' in the project 
    root and publish them to a folder called 'docs' in the ``MEDIA_ROOT`` of 
    your settings file. You can override these with the following project
    settings:
    
        DOCUMENTATION_PUBLISH_PATH = '/path/to/publish/to/'
        DOCUMENTATION_SOURCE_LOCATION = '/docs/source/path/'
    
    """
    
    help = 'Builds the documentation for this Django project.'

    
    def __init__(self):
        # The docstring doubles as the help.
        self.help = self.__doc__
        return super(Command, self).__init__()
    
    def handle(self, *args, **options):
        try:
            subprocess.check_call([
                'sphinx-build',
                '-b',
                'html',
                app_settings.SOURCE_LOCATION,
                app_settings.PUBLISH_PATH
            ])
        except subprocess.CalledProcessError, e:
            self.stdout.write((
                "Docs failed to publish to: %s Are you sure that the "
                "documents source location is correct and the publish path "
                "is writable?\n"
            )% app_settings.PUBLISH_PATH)
        except OSError, e:
            if e[0] == 2:
                err = (
                    "Error: sphinx-build could not be found. Are you sure "
                    "Sphinx is installed?\n"
                )
            else:
                err = e[1] + "\n"
            self.stdout.write(err)            
        else:       
            self.stdout.write(
                "Docs published to: %s.\n" % app_settings.PUBLISH_PATH
            )
