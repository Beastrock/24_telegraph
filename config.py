import os.path

# directories
base_directory = os.path.abspath(os.path.dirname(__file__))

# The CSRF_ENABLED setting activates the cross-site request forgery prevention
CSRF_ENABLED = True

# The SECRET_KEY setting is only needed when CSRF is enabled,
# and is used to create a cryptographic token that is used to validate a form.
SECRET_KEY = 'you-will-never-guess-dope'

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_directory, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(base_directory, 'db_repository')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True