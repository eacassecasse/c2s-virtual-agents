#!/usr/bin/python3
"""
Complete self-adapting DataSeeder that automatically detects all fields
"""
import enum
import uuid
import inspect
from datetime import datetime, UTC
from random import choice, randint, uniform
from faker import Faker
from typing import Dict, List, Type, Any, get_type_hints, Union, Optional

import app.models


class DataSeeder:
    """Automatically adapts to any model's fields without configuration"""

    def __init__(self, number_of_records=100):
        self.number_of_records = number_of_records
        self.faker = Faker()

        # Enhanced type generators
        self.type_generators = {
            str: {
                'default': lambda: self.faker.word(),
                'patterns': {
                    'email': lambda: self.faker.email(),
                    'name': lambda: self.faker.word().title(),
                    'color': lambda: self.faker.color_name(),
                    'description': lambda: self.faker.text(max_nb_chars=200),
                    'text': lambda: self.faker.text(max_nb_chars=200),
                    'phone': lambda: self.faker.phone_number(),
                    'address': lambda: self.faker.address(),
                    'plate': lambda: self._generate_license_plate(),
                    'number': lambda: str(randint(1000, 9999)),
                }
            },
            int: {
                'default': lambda: randint(1, 10000),
                'patterns': {
                    'year': lambda: randint(1990, datetime.now(UTC).year),
                    'mileage': lambda: randint(0, 200000),
                    'quantity': lambda: randint(1, 100),
                }
            },
            float: {
                'default': lambda: round(uniform(0, 1000), 2),
                'patterns': {
                    'price': lambda: round(uniform(1, 100000), 2),
                    'weight': lambda: round(uniform(1, 1000), 2),
                }
            },
            bool: {
                'default': lambda: self.faker.boolean()
            },
            datetime: {
                'default': lambda: datetime.now(UTC)
            }
        }

    @staticmethod
    def camel_to_snake(camel_str: str) -> str:
        """
        Convert camelCase string to snake_case.

        Args:
            camel_str: Input string in camelCase format

        Returns:
            String converted to snake_case

        Examples:
            >>> DataSeeder.camel_to_snake("vehicleModel")
            'vehicle_model'
            >>> DataSeeder.camel_to_snake("HTTPResponse")
            'http_response'
            >>> DataSeeder.camel_to_snake("userID")
            'user_id'
        """
        snake_str = []
        for i, char in enumerate(camel_str):
            if char.isupper():
                # Add underscore if not at start and previous character isn't underscore
                if i > 0 and snake_str[-1] != '_':
                    snake_str.append('_')
                snake_str.append(char.lower())
            else:
                snake_str.append(char)
        return ''.join(snake_str)

    def generate_data(self, model_class: Type, count: int = None, **overrides) -> List[Dict]:
        """Generates fake data for any model class"""
        count = count or self.number_of_records
        return [self._generate_single_record(model_class, overrides) for _ in range(count)]

    def _generate_single_record(self, model_class: Type, overrides: Dict) -> Dict:
        """Generates a complete record with all detected fields"""
        record = {}

        # Get all fields including SQLAlchemy columns and regular attributes
        fields = self._get_model_fields(model_class)

        for field_name, field_type in fields.items():
            if field_name in {'id', 'created_at', 'updated_at'}:
                continue

            if field_name in overrides:
                record[field_name] = overrides[field_name]
                continue

            record[field_name] = self._generate_field_value(field_name, field_type)

        return record

    def _get_model_fields(self, model_class: Type) -> Dict[str, Type]:
        """Gets all fields including SQLAlchemy columns and type hints"""
        fields = {}

        # Get SQLAlchemy columns if present
        if hasattr(model_class, '__table__'):
            for column in model_class.__table__.columns:
                fields[column.name] = column.type.python_type if hasattr(column.type, 'python_type') else str

        # Get type hints (for non-column fields)
        type_hints = get_type_hints(model_class)
        for field_name, field_type in type_hints.items():
            if field_name not in fields:  # Don't override SQLAlchemy columns
                fields[field_name] = field_type

        # Get regular attributes (as fallback)
        for attr_name in dir(model_class):
            if not attr_name.startswith('_') and attr_name not in fields:
                attr = getattr(model_class, attr_name)
                if not inspect.isfunction(attr) and not inspect.ismethod(attr):
                    fields[attr_name] = type(attr) if attr else str

        return fields

    def _generate_field_value(self, field_name: str, field_type: Type) -> Any:
        """Intelligently generates values based on field name and type"""
        # Handle enum fields
        if isinstance(field_type, type) and issubclass(field_type, enum.Enum):
            return choice(list(field_type)).value

        if field_name == "registration_date":
            return self._generate_registration_date()

        if field_name == "year_of_manufacture":
            return self.type_generators[int]['patterns']['year']()

        # Handle Optional[T] and Union types
        if hasattr(field_type, '__origin__'):
            if field_type.__origin__ == Union:
                # Get the first non-None type
                actual_type = next(t for t in field_type.__args__ if t != type(None))  # noqa
                return self._generate_field_value(field_name, actual_type)

        # Get the base type for containers
        base_type = field_type.__origin__ if hasattr(field_type, '__origin__') else field_type

        # Find matching generator
        type_generators = self.type_generators.get(base_type, {})

        # Try field name patterns first
        if 'patterns' in type_generators:
            field_lower = field_name.lower()
            for pattern, generator in type_generators['patterns'].items():
                if pattern in field_lower:
                    return generator()

        # Fall back to type default
        if 'default' in type_generators:
            return type_generators['default']()

        # Special cases for SQLAlchemy types
        if str(field_type).endswith('UUID'):
            return str(uuid.uuid4())
        if str(field_type).endswith('DateTime'):
            return datetime.now(UTC)

        # Final fallbacks
        if inspect.isclass(base_type) and issubclass(base_type, (list, dict, set)):
            return base_type()

        return None

    # Special field generators
    def _generate_license_plate(self) -> str:
        return f"{self.faker.random_uppercase_letter()}{self.faker.random_uppercase_letter()}-" \
               f"{randint(100, 999)}-{self.faker.random_uppercase_letter()}{self.faker.random_uppercase_letter()}"

    def _generate_registration_date(self) -> Optional[datetime | str]:
        """Generate registration date (30% chance of being None)"""
        if randint(1, 10) <= 3:  # 30% chance to be None
            return None
        dt = datetime.combine(
            self.faker.date_between(start_date='-10y', end_date='today'),
            self.faker.time_object(),
            tzinfo=UTC
        )

        if app.models.storage_t == "db":
            return dt

        return dt.isoformat()

    def _generate_engine_number(self) -> str:
        return f"ENG{randint(1000000, 9999999)}"

    def _generate_chassis_number(self) -> str:
        return f"{self.faker.random_uppercase_letter()}{randint(100000000000, 999999999999)}"

    def generate_related_data(self, parent_class: Type, child_class: Type,
                              count: int = None, parent_records: List = None,
                              **overrides) -> List[Dict]:
        """Generates related data with automatic foreign key detection"""
        count = count or self.number_of_records
        child_data = self.generate_data(child_class, count, **overrides)

        if parent_records:
            fk_field = self._detect_foreign_key_field(child_class, parent_class)
            for data in child_data:
                data[fk_field] = choice(parent_records).id

        return child_data

    def _detect_foreign_key_field(self, child_class: Type, parent_class: Type) -> str:
        """Automatically detects the foreign key field name"""
        parent_class = DataSeeder.camel_to_snake(parent_class.__name__)
        parent_name = parent_class.lower()

        # Check common naming patterns
        possible_fields = [
            f"{parent_name}_id",
            f"{parent_name[:-1]}_id",  # For singular (e.g., "brand_id" from "Brands")
            "parent_id",
            f"{parent_name}_fk",
            f"{parent_name}id"
        ]

        fields = self._get_model_fields(child_class)
        for field in possible_fields:
            if field in fields:
                return field

        # Fallback to any field ending with "_id" that matches parent name
        for field in fields:
            if field.endswith('_id') and parent_name in field.lower():
                return field

        raise ValueError(f"Could not detect foreign key field in {child_class.__name__} "
                         f"for relationship with {parent_class.__name__}")
