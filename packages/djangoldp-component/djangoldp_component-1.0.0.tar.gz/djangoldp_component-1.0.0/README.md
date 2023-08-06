# Django LDP component package

## Step by step quickstart

1. Installation

- `git clone git@git.startinblox.com:applications/ontochain/component-registry.git /path/to/myawesomepackage`

NB:

- replace /path/to/myawesomepackage with the local path of your package.
- replace the_repository_url with the git url of your package (example: git@git.happy-dev.fr:startinblox/djangoldp-packages/djangoldp-component.git).
- replace djangoldp*myawesomepackage with your package name. Please respect the naming convention (singular word, starting by `djangoldp*`)

2. Developpement environnement

In order to test and developp your package, you need to put the package src directory at the same level of a working django ldp app. By exemple, you can clone the sib app data server
`git clone git@git.startinblox.com:applications/ontochain/component-registry.git server /path/to/app`

- The classical way :
  `ln -s /path/to/myawesomepackage/djangoldp_myawesomepackage /path/to/app/djangoldp_myawesomepackage`

- The docker way : in the _volumes_ section, add a line in docker-compose.override.yml. Example

```yaml
volumes:
  - ./:/app
  - /path/to/myawesomepackage/djangoldp_myawesomepackage:/app/djangoldp_myawesomepackage
```

Add your package in settings.py of the app. Now, you can test if your package is imported propefully by doing a
`python manage.py shell` then
from djangoldp_myawesomepackage.models import ExampleModel

If, no error, it's working.

3. Customization

- `setup.cfg` : please, fill the name, version, url, author_email, description
- `djangoldp_component/__init__.py`: fill the name, don't touch the version number !

4. Push on the repository you've created
