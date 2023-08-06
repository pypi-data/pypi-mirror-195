# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whylabs_toolkit',
 'whylabs_toolkit.cli',
 'whylabs_toolkit.container',
 'whylabs_toolkit.helpers',
 'whylabs_toolkit.monitor',
 'whylabs_toolkit.monitor.manager',
 'whylabs_toolkit.monitor.models',
 'whylabs_toolkit.monitor.models.analyzer']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0',
 'types-pytz>=2022.7.1.0,<2023.0.0.0',
 'whylabs-client>=0.4.2,<0.5.0',
 'whylogs>=1.1.26,<2.0.0']

setup_kwargs = {
    'name': 'whylabs-toolkit',
    'version': '0.0.2',
    'description': 'Whylabs CLI and Helpers package.',
    'long_description': '# WhyLabs Toolkit\n\nThe WhyLabs Toolkit package contains helper methods to help users interact with our internal APIs. Users will benefit from using it if they want to abstract some of WhyLabs\' internal logic and also automate recurring API calls.\n\n## Configuration\nIn order to configure `whylabs_toolkit`, you will need to set `WHYLABS_API_KEY` as an environment variable. With that, the package will be able to authenticate with WhyLabs\' API endpoints. You can configure a token for your account directly on the platform. \n\nTo manage dependencies we use [Poetry](https://python-poetry.org/) and also a handful of `Makefile` commands. To install all necessary dependencies and activate the virtual environment, run:\n\n```bash\nmake setup && poetry shell\n```\n\n## Usage\nIn here we will describe some examples on how to use the package. You can also check [the integration tests directory](./tests/) to have more insights on how things are built to be used.\n### Models\nUsers can change their model type between `REGRESSION`, `CLASSIFICATION` and `EMBEDDINGS`, using the models helpers, as the example shows:\n```python\nfrom whylabs_toolkit.helpers.models import update_model_metadata\n\nupdate_model_metadata(\n    org_id="org_id",\n    dataset_id="dataset_id",\n    model_type="CLASSIFICATION"\n)\n```\n\nAnd to change the model granularity:\n\n```python\nfrom whylabs_toolkit.helpers.models import update_model_metadata\n\nupdate_model_metadata(\n    dataset_id="dataset_id", \n    org_id="org_id", \n    time_period="P1M"\n)\n```\n\n>**NOTE**: Learn more on the time period config options with the `whylabs_client.model.time_period.TimePeriod` class, available after you\'ve configured your environment with the described make command above.\n\n### Entity Schema\nEntity Schema helpers assist users to change some of their dataset metadata, such as data types, discreteness and column classification (between inputs and outputs). Here\'s an example that covers all three cases:\n\n#### Column Classes\n```python\nfrom whylabs_toolkit.helpers.schema import (\n    UpdateColumnClassifiers, \n    ColumnsClassifiers,\n)\n\n# Note that you don\'t need to specify all existing columns, but only those you wish to modify\n\nclassifiers = ColumnsClassifiers(\n    outputs=["actual_temperature", "predicted_temperature"]\n)\n\nupdate_entity = UpdateColumnClassifiers(\n    classifiers=classifiers,\n    dataset_id="dataset_id",\n    org_id="org_id"\n)\n\nupdate_entity.update()\n\n```\n#### Data types\n```python\nfrom whylabs_toolkit.helpers.schema import UpdateEntityDataTypes\nfrom whylabs_toolkit.monitor_schema.models.column_schema import ColumnDataType\n\ncolumns_schema = {\n    "temperature": ColumnDataType.fractional,\n    "is_active": ColumnDataType.boolean\n}\n\nupdate_data_types = UpdateEntityDataTypes(\n    dataset_id="dataset_id",\n    columns_schema=columns_schema,\n    org_id="org_id"\n)\n\nupdate_data_types.update()\n```\n#### Discreteness\n```python\nfrom whylabs_toolkit.helpers.schema import (\n    UpdateColumnsDiscreteness,\n    ColumnsDiscreteness\n)\n\ncolumns = ColumnsDiscreteness(\n    discrete=["temperature"]\n)\n\nupdate_discreteness = UpdateColumnsDiscreteness(\n    dataset_id="dataset_id",\n    columns=columns,\n    org_id="org_id"\n)\n\nupdate_discreteness.update()\n```\n### Monitors\nThe Monitors helpers will help you manage existing alerts on WhyLabs\' platform.\n\n#### Delete monitor\n\n```python\nfrom whylabs_toolkit.helpers.monitor_helpers import delete_monitor\n\ndelete_monitor(\n    org_id="org_id",\n    dataset_id="dataset_id",\n    monitor_id="monitor_id"\n)\n```\n\n## Get in touch\nIf you want to learn more how you can benefit from this package or if there is anything missing, please [contact our support](https://whylabs.ai/contact-us), we\'ll be more than happy to help you!',
    'author': 'Anthony Naddeo',
    'author_email': 'anthony.naddeo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
