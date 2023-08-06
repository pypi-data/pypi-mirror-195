import pypandoc
from setuptools import setup

setup(
    name='kicad_gitdiff',
    version='0.0.1',
    url='https://github.com/maersdal/kicad_gitdiff_cli',
    license='Apache-2.0',
    license_files=["LICENSE"],
    author='magnus ersdal',
    author_email='magnus@resani.com',
    description='A tool for a visual diff with git and kicad',
    long_description=open("project_description.md",'r').read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=['git_config_template', 'kicad_export', 'sch_diff', 'svg_diff', 'checkers'],
    package_data={"git_config_template": ["*_template"]},
    include_package_data=True,
    entry_points={
        'console_scripts':
            ['kdiff_initialize = git_config_template:append_custom_git_config',
             'kicad_sch_diff = sch_diff:git_diff',
             ]
        },
    )
