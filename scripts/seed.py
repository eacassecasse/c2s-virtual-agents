#!/usr/bin/python3
"""
Seeds the storage with fake data
"""
from sqlalchemy.exc import SQLAlchemyError

from app.models import storage
from app.db.data_seeder import DataSeeder
from app.models.brand import Brand
from app.models.vehicle_model import VehicleModel
from app.models.vehicle import Vehicle


def run_seed():
    """
    Seeds the storage with fake data
    :return: void
    """
    seeder = DataSeeder()

    try:
        storage.start_transaction()

        print("Cleaning existing data...")
        storage.delete_all(Vehicle)
        storage.delete_all(VehicleModel)
        storage.delete_all(Brand)

        print("Generating brands data...")
        brands_data = seeder.generate_data(Brand)

        print("Persisting brands data...")
        for brand_data in brands_data:
            brand = Brand(**brand_data)
            storage.new(brand)

        print("Fetching brands from the storage...")
        brands = list(storage.all(Brand).values())

        print("Generating vehicle models data...")
        models_data = seeder.generate_related_data(parent_class=Brand,
                                                   child_class=VehicleModel,
                                                   parent_records=brands)

        print("Persisting vehicle models data...")
        for model_data in models_data:
            vehicle_model = VehicleModel(**model_data)
            storage.new(vehicle_model)

        print("Fetching vehicle models from the storage...")
        vehicle_models = list(storage.all(VehicleModel).values())

        print("Generating vehicles data...")
        vehicles_data = seeder.generate_related_data(parent_class=VehicleModel,
                                                     child_class=Vehicle,
                                                     parent_records=vehicle_models)

        print("Persisting vehicles data...")
        for vehicle_data in vehicles_data:
            vehicle = Vehicle(**vehicle_data)
            storage.new(vehicle)

        storage.commit()
        print("Seeding completed successfully!")
    except SQLAlchemyError as er:
        storage.rollback()
        print(f"Data insertion failure {str(er)}")
        raise er
    except Exception as ex:
        storage.rollback()
        print(f"Unexpected error {str(ex)}")
        raise
    finally:
        storage.close()


if __name__ == "__main__":
    run_seed()
