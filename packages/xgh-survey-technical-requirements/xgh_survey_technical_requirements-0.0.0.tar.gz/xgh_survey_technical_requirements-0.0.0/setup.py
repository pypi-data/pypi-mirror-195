from setuptools import setup, find_packages

setup(
    name='xgh_survey_technical_requirements',
    author='xgh',
    description='生成勘察报告技术要求',
    version='0.0.0',
    packages=find_packages(exclude=['tests', 'testing']),
    entry_points={
        'console_scripts': [
            'x-generate-survey-requitements=survey_technical_requirements.main:main'
        ]
    }
)
