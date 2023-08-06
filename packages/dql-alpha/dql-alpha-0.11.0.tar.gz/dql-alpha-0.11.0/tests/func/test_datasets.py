import sqlite3
import uuid

import pytest


@pytest.fixture
def cats_shadow_dataset(cloud_test_catalog):
    shadow_dataset_name = uuid.uuid4().hex
    src_uri = cloud_test_catalog.src_uri
    catalog = cloud_test_catalog.catalog

    # list source to have it in db as source for dataset
    list(
        catalog.ls(
            [src_uri],
            client_config=cloud_test_catalog.client_config,
        )
    )

    catalog.upsert_shadow_dataset(
        shadow_dataset_name,
        [f"{src_uri}/cats/*"],
        client_config=cloud_test_catalog.client_config,
        recursive=True,
    )

    return catalog.data_storage.get_dataset(shadow_dataset_name)


@pytest.fixture
def dogs_shadow_dataset(cloud_test_catalog):
    shadow_dataset_name = uuid.uuid4().hex
    src_uri = cloud_test_catalog.src_uri
    catalog = cloud_test_catalog.catalog

    # list source to have it in db as source for dataset
    list(
        catalog.ls(
            [src_uri],
            client_config=cloud_test_catalog.client_config,
        )
    )

    catalog.upsert_shadow_dataset(
        shadow_dataset_name,
        [f"{src_uri}/dogs/*"],
        client_config=cloud_test_catalog.client_config,
        recursive=True,
    )

    return catalog.data_storage.get_dataset(shadow_dataset_name)


@pytest.fixture
def dogs_registered_dataset(cloud_test_catalog, dogs_shadow_dataset):
    catalog = cloud_test_catalog.catalog
    catalog.register_shadow_dataset(
        dogs_shadow_dataset.name,
        description="dogs dataset",
        labels=["dogs", "dataset"],
    )

    return catalog.data_storage.get_dataset(dogs_shadow_dataset.name)


@pytest.fixture
def cats_registered_dataset(cloud_test_catalog, cats_shadow_dataset):
    catalog = cloud_test_catalog.catalog
    catalog.register_shadow_dataset(
        cats_shadow_dataset.name,
        description="cats dataset",
        labels=["cats", "dataset"],
    )

    return catalog.data_storage.get_dataset(cats_shadow_dataset.name)


def test_upserting_shadow_dataset(cloud_test_catalog):
    shadow_dataset_name = uuid.uuid4().hex
    src_uri = cloud_test_catalog.src_uri
    catalog = cloud_test_catalog.catalog

    # list source to have it in db as source for dataset
    list(
        catalog.ls(
            [src_uri],
            client_config=cloud_test_catalog.client_config,
        )
    )

    catalog.upsert_shadow_dataset(
        shadow_dataset_name,
        [f"{src_uri}/dogs/*"],
        client_config=cloud_test_catalog.client_config,
        recursive=True,
    )

    dataset = catalog.data_storage.get_dataset(shadow_dataset_name)
    assert dataset.name == shadow_dataset_name
    assert dataset.description is None
    assert dataset.versions is None
    assert dataset.labels == []
    assert dataset.shadow is True

    dataset_table_name = catalog.data_storage._dataset_table_name(dataset.id)
    data = catalog.data_storage.db.execute(
        f"select * from {dataset_table_name}"
    ).fetchall()
    assert data


def test_registering_dataset(cloud_test_catalog, dogs_shadow_dataset):
    catalog = cloud_test_catalog.catalog

    catalog.register_shadow_dataset(
        dogs_shadow_dataset.name,
        description="dogs dataset",
        labels=["dogs", "dataset"],
    )

    dataset = catalog.data_storage.get_dataset(dogs_shadow_dataset.name)
    dataset_table_name = catalog.data_storage._dataset_table_name(dataset.id, 1)
    assert dataset.name == dogs_shadow_dataset.name
    assert dataset.description == "dogs dataset"
    assert dataset.versions == [1]
    assert dataset.labels == ["dogs", "dataset"]
    assert dataset.shadow is False
    data = catalog.data_storage.db.execute(
        f"select * from {dataset_table_name}"
    ).fetchall()
    assert data


def test_registering_dataset_with_new_name(cloud_test_catalog, dogs_shadow_dataset):
    new_dataset_name = uuid.uuid4().hex
    catalog = cloud_test_catalog.catalog

    catalog.register_shadow_dataset(
        dogs_shadow_dataset.name,
        registered_name=new_dataset_name,
        description="dogs dataset",
        labels=["dogs", "dataset"],
    )
    dataset = catalog.data_storage.get_dataset(new_dataset_name)
    assert dataset
    dataset_table_name = catalog.data_storage._dataset_table_name(dataset.id, 1)
    assert dataset.name == new_dataset_name
    data = catalog.data_storage.db.execute(
        f"select * from {dataset_table_name}"
    ).fetchall()
    assert data


def test_registering_dataset_with_custom_version(
    cloud_test_catalog, dogs_shadow_dataset
):
    catalog = cloud_test_catalog.catalog

    catalog.register_shadow_dataset(
        dogs_shadow_dataset.name,
        version=5,
        description="dogs dataset",
        labels=["dogs", "dataset"],
    )

    dataset = catalog.data_storage.get_dataset(dogs_shadow_dataset.name)
    assert dataset.versions == [5]


def test_registering_dataset_as_version_of_another_registered(
    cloud_test_catalog, dogs_registered_dataset, cats_shadow_dataset
):
    catalog = cloud_test_catalog.catalog

    catalog.register_shadow_dataset(
        cats_shadow_dataset.name,
        registered_name=dogs_registered_dataset.name,
        version=3,
    )

    dogs_dataset = catalog.data_storage.get_dataset(dogs_registered_dataset.name)
    assert dogs_dataset.versions == [1, 3]
    # checking newly created dogs version 3 data
    assert {
        r.name for r in catalog.ls_dataset_rows(dogs_registered_dataset.name, version=3)
    } == {
        "cat1",
        "cat2",
    }

    # assert cats shadow dataset is removed
    cats_dataset_name = catalog.data_storage._dataset_table_name(cats_shadow_dataset.id)
    cats_shadow_dataset = catalog.data_storage.get_dataset(cats_shadow_dataset.name)
    assert cats_shadow_dataset is None
    with pytest.raises(sqlite3.OperationalError):
        catalog.data_storage.db.execute(f"select * from {cats_dataset_name}").fetchall()


def test_removing_dataset(cloud_test_catalog, dogs_shadow_dataset):
    catalog = cloud_test_catalog.catalog

    dataset_table_name = catalog.data_storage._dataset_table_name(
        dogs_shadow_dataset.id
    )
    data = catalog.data_storage.db.execute(
        f"select * from {dataset_table_name}"
    ).fetchall()
    assert data

    catalog.remove_dataset(dogs_shadow_dataset.name)
    dataset = catalog.data_storage.get_dataset(dogs_shadow_dataset.name)
    assert dataset is None
    with pytest.raises(sqlite3.OperationalError):
        catalog.data_storage.db.execute(
            f"select * from {dataset_table_name}"
        ).fetchall()


def test_edit_dataset(cloud_test_catalog, dogs_registered_dataset):
    dataset_new_name = uuid.uuid4().hex
    catalog = cloud_test_catalog.catalog

    catalog.edit_dataset(
        dogs_registered_dataset.name,
        new_name=dataset_new_name,
        description="new description",
        labels=["cats", "birds"],
    )

    dataset = catalog.data_storage.get_dataset(dataset_new_name)
    assert dataset.versions == [1]
    assert dataset.name == dataset_new_name
    assert dataset.description == "new description"
    assert dataset.labels == ["cats", "birds"]


def test_ls_dataset_rows(cloud_test_catalog, dogs_registered_dataset):
    catalog = cloud_test_catalog.catalog

    assert {
        r.name for r in catalog.ls_dataset_rows(dogs_registered_dataset.name, version=1)
    } == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    }


def test_merge_datasets_shadow_to_registered(
    cloud_test_catalog, dogs_registered_dataset, cats_shadow_dataset
):
    catalog = cloud_test_catalog.catalog
    catalog.merge_datasets(
        cats_shadow_dataset.name, dogs_registered_dataset.name, dst_version=2
    )

    dogs_dataset = catalog.data_storage.get_dataset(dogs_registered_dataset.name)
    assert dogs_dataset.versions == [1, 2]

    # making sure version 1 is not changed
    assert {
        r.name for r in catalog.ls_dataset_rows(dogs_registered_dataset.name, version=1)
    } == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
    }

    assert {
        r.name for r in catalog.ls_dataset_rows(dogs_registered_dataset.name, version=2)
    } == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
        "cat1",
        "cat2",
    }


def test_merge_datasets_registered_to_registered(
    cloud_test_catalog, dogs_registered_dataset, cats_registered_dataset
):
    catalog = cloud_test_catalog.catalog
    catalog.merge_datasets(
        cats_registered_dataset.name,
        dogs_registered_dataset.name,
        src_version=1,
        dst_version=2,
    )

    dogs_dataset = catalog.data_storage.get_dataset(dogs_registered_dataset.name)
    assert dogs_dataset.versions == [1, 2]

    assert {
        r.name for r in catalog.ls_dataset_rows(dogs_registered_dataset.name, version=2)
    } == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
        "cat1",
        "cat2",
    }


def test_merge_datasets_shadow_to_shadow(
    cloud_test_catalog, dogs_shadow_dataset, cats_shadow_dataset
):
    catalog = cloud_test_catalog.catalog
    catalog.merge_datasets(
        cats_shadow_dataset.name,
        dogs_shadow_dataset.name,
    )

    dogs_dataset = catalog.data_storage.get_dataset(dogs_shadow_dataset.name)
    assert dogs_dataset.shadow is True  # dataset stays shadow

    assert {r.name for r in catalog.ls_dataset_rows(dogs_shadow_dataset.name)} == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
        "cat1",
        "cat2",
    }


def test_merge_datasets_registered_to_shadow(
    cloud_test_catalog, dogs_shadow_dataset, cats_registered_dataset
):
    catalog = cloud_test_catalog.catalog
    catalog.merge_datasets(
        cats_registered_dataset.name,
        dogs_shadow_dataset.name,
        src_version=1,
    )

    dogs_dataset = catalog.data_storage.get_dataset(dogs_shadow_dataset.name)
    assert dogs_dataset.shadow is True  # dataset stays shadow

    assert {r.name for r in catalog.ls_dataset_rows(dogs_shadow_dataset.name)} == {
        "dog1",
        "dog2",
        "dog3",
        "dog4",
        "cat1",
        "cat2",
    }
