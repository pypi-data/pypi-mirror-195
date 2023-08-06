# Task Analytics Data Wrapper

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a wrapper for Task Analytics APIs. You can use it to download survey responses and metadata for each survey.

## Supported APIs

- [Task Analytics Data Wrapper](#task-analytics-data-wrapper)
  - [Supported APIs](#supported-apis)
    - [Log in to Task Analytics](#log-in-to-task-analytics)
    - [Download Survey responses](#download-survey-responses)
    - [Download Survey metadata](#download-survey-metadata)

### Log in to Task Analytics

You can log in with email and password

```python
status = log_in_taskanalytics(username=email, password=password)  
status.status_code
```

### Download Survey responses

You can download survey responses for a Top Task survey using the survey ID, email, password and setting a path for where to store the file.

```python
get_survey = download_survey(
    username=email, password=password, survey_id="03324", filename="data/survey.csv"
)
get_survey.status_code
```

### Download Survey metadata

You can download the survey metadata which includes the questions and response options for each survey using the survey ID, email and password.

```python
survey_metadata = get_survey_metadata(
    username=email, password=password, survey_id="03324"
)
survey_metadata.status_code
```

The object can be easily inspected transformed into a dictionary for analysis

```python
survey_metadata.text # survey metadata
our_dict = survey_metadata.json() # convert string to dict and store as a variable
```