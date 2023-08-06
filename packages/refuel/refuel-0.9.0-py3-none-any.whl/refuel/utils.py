from datetime import datetime, timedelta, timezone
from typing import Dict
from jsonschema import validators, Draft7Validator
from loguru import logger
import re

REFUEL_DATE_FORMAT = "%Y-%m-%d"


def is_valid_uri(checker, uri):
    # check if valid S3 URI
    if uri.startswith("s3://") or uri.startswith("s3a://"):
        return True
    # check if valid GCS URI
    if uri.startswith("gs://"):
        return True
    # Regular expression pattern to match other URLs
    url_pattern = r"^(https?|ftp)://[^\s/$.?#].[^\s]*$"
    if re.match(url_pattern, uri):
        return True
    return False


def is_valid_detection_2d(checker, detect2d):
    if type(detect2d) is not dict:
        return False
    if detect2d.get("annotations") is None:
        return False
    if not isinstance(detect2d.get("annotations"), list):
        return False
    return True


def validate_event_schema(event: Dict, schema: Dict):
    validator = validators.extend(Draft7Validator)
    type_checker = validator.TYPE_CHECKER
    type_checker = type_checker.redefine("uri", is_valid_uri)
    type_checker = type_checker.redefine("detection 2d", is_valid_detection_2d)
    validator = validators.extend(Draft7Validator, type_checker=type_checker)
    try:
        validator(schema).validate(event)
        return True
    except Exception as exp:
        logger.error(f"Schema validation failed for event: {exp}")
        return False


def to_date_string(date_obj, fmt=REFUEL_DATE_FORMAT):
    return datetime.strftime(date_obj, fmt)


def get_datetime_offset(datetime_obj: datetime, delta: timedelta):
    return datetime_obj + delta


def current_utc_time():
    return datetime.now(timezone.utc)


DATE_FOURTEEN_DAYS_AGO = to_date_string(
    get_datetime_offset(current_utc_time(), -timedelta(days=14))
)
DATE_TOMORROW = to_date_string(
    get_datetime_offset(current_utc_time(), timedelta(days=1))
)
