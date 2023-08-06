# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['better_safe_than_sorry',
 'better_safe_than_sorry.analysis',
 'better_safe_than_sorry.generation_of_test_profiles',
 'better_safe_than_sorry.shared',
 'better_safe_than_sorry.simulation',
 'better_safe_than_sorry.utils',
 'better_safe_than_sorry.vagrant_deployment']

package_data = \
{'': ['*']}

install_requires = \
['pyeda==0.28.0', 'scikit-learn>=1.0.1,<2.0.0', 'typer>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['better-safe-than-sorry = better_safe_than_sorry:app',
                     'bsts = better_safe_than_sorry:app']}

setup_kwargs = {
    'name': 'better-safe-than-sorry',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Better Safe Than Sorry\n\nThis repository is part of the paper *Better Safe Than Sorry! Automated Identification of Breaking Security-Configuration Rules* accepted at the [4th ACM/IEEE International Conference on Automation of Software Test (AST)](https://conf.researchr.org/home/ast-2023).\n\nInstitutions like the [Center for Internet Security](https://www.cisecurity.org/) publish security-configuration guides(also called benchmarks) that help us configure systems more securely.\nThis configuration hardening can mitigate the risk of successful attacks, which may cause damage to our systems and data.\nA remaining problem with applying these guides are so-called "breaking rules."\nApplying breaking rules on a production system will break at least one functionality with the corresponding ramifications.\nWe could safely apply the remaining rules if we identified all breaking rules and removed them from the guide.\n\nOur new approach combines techniques from software testing, machine learning, and graph theory to automatically identify these breaking rules.\nThis repository includes our Python scripts to\n\n1. generate the covering arrays from a given security-configuration guide\n2. Test the different covering arrays\n3. Analyze the results to find the breaking rules\n\nOne can redo all our experiments presented in the article using the code in this repository.\n\n## Setup\n\n### With PyPi\n\nThe easiest way to use the scrips in this repository is to install the package from PyPi\n\n```shell\npip install better-safe-than-sorry\nbetter-safe-than-sorry --version\n```\n\n### With Poetry\n\nOne can also use poetry to install the dependencies.\n\n```shell\ncd /path/to/better-safe-than-sorry/\npoetry install\npoetry run better-safe-than-sorry --version\n```\n\n## Steps\n\n### Generate Profiles based on Covering Arrays\n\nSee [here](better_safe_than_sorry/generation_of_test_profiles/README.md).\n\n### Test Execution\n\n#### Simulation\n\nSee [here](better_safe_than_sorry/simulation/README.md).\n\n#### Test Execution with Vagrant\n\nSee [here](better_safe_than_sorry/vagrant_deployment/README.md)\n\n### Test Result Analysis\n\nSee [here](better_safe_than_sorry/analysis/README.md).\n\n## Resources\n\n### Sfera Automation files\n\nThe folder [rsc/sfera_automation_jsons](rsc/sfera_automation_jsons) contains variants of `sfera_automation.json` files based on the Windows 10 version 1909 guide by the Center for Internet Security.\n`sfera_automation.json` is a JSON-based file format used at Siemens to automatically implement Windows-based security-configuration guides.\nWe generated the variants were generated using the IPOG and IPOG-D algorithms and include custom profiles for combinatorial testing of strength 2 to 5.\n\n## Contact\n\nIf you have any questions, please create an issue or contact [Patrick Stöckle](mailto:patrick.stoeckle@tum.de?subject=GitHub%20Repository%20%22better-safe-than-sorry%22).\n',
    'author': 'Michael Sammereier',
    'author_email': 'michael.sammereier@tum.de',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@tum.de',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
