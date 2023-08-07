import json
import os
from typing import List

from pathlib import Path

from knapsack.knapsack_dataset import KnapsackDataset
from knapsack.kd_builder import KDBuilder, Split
from knapsack.account import post


class TestKnapsack(object):
    API_KEY_LOCATION = os.path.expanduser("~/.knapsack_local/api_keys/test_api_key")
    SERVER_CONFIG_LOCATION = "./config/server.json"

    LOCAL_KNAPSACK_STORAGE_LOCATION = Path(os.path.expanduser("~/.knapsack_local/storage"))
    REMOTE_KNAPSACK_STORAGE_LOCATION = Path(os.path.expanduser("~/.knapsack_remote/storage"))

    @classmethod
    def setup_class(cls):
        cls.org_name = "knap_tester"
        with open(cls.SERVER_CONFIG_LOCATION, "r") as f:
            server_config = json.load(f)
            cls.server_config = server_config

    @classmethod
    def teardown_class(cls):
        # os.remove(cls.API_KEY_LOCATION)
        pass

    def test_account_setup_endpoints(self):
        response = post(
            endpoint="create_user",
            user_name="cooper",
            email="cooperlindsey3927@gmail.com",
            first_name="Cooper",
            last_name="Lindsey",
        )
        print("create_user response: ", response.json())
        assert response.json()['status'] == 0

        response = post(
            endpoint="create_org",
            org_name=self.org_name,
            creator_user_name="cooper",
        )
        print("create_org response: ", response.json())
        assert response.json()['status'] == 0

        response = post(
            endpoint="create_api_key",
            org_name=self.org_name,
        )
        api_key = response.json()['apiKey']
        if not Path(self.API_KEY_LOCATION).exists():
            parent_dir = Path(self.API_KEY_LOCATION).parents[0]
            parent_dir.mkdir(parents=True, exist_ok=True)
        with open(self.API_KEY_LOCATION, 'w') as f:
            f.write(api_key)
        print("create_api_key response: ", response.json())
        assert response.json()['status'] == 0

    def test_knapsack_basic_ops(self):
        salmon_dataset = self._test_store(org_name=self.org_name, dataset_name="salmon")
        repro_tag = salmon_dataset.repro_tag
        starting_size = len(salmon_dataset)

        orig_filenames = self._get_list_of_all_filenames_in_dir(
            self.LOCAL_KNAPSACK_STORAGE_LOCATION / Path(self.org_name))
        self._remove_all_files_in_local_knapsack()

        salmon_dataset = self._test_procure(dataset_name="salmon")
        new_filenames = self._get_list_of_all_filenames_in_dir(
            self.LOCAL_KNAPSACK_STORAGE_LOCATION / Path(self.org_name))
        diff = list(set(orig_filenames) - set(new_filenames))
        assert len(diff) == 0
        diff = list(set(new_filenames) - set(orig_filenames))
        assert len(diff) == 0

        salmon_dataset = self._test_procure(dataset_name="salmon")
        procured_repro_tag = salmon_dataset.repro_tag

        assert repro_tag == procured_repro_tag

        self._test_append(salmon_dataset, "salmon")
        repro_tag_after_append = salmon_dataset.repro_tag
        assert repro_tag_after_append != procured_repro_tag
        assert len(salmon_dataset) > starting_size

        self.test_dataset = salmon_dataset
        # salmon_dataset2 = self._test_store(
        #     org_name=self.org_name,
        #     dataset_name="not_salmon"
        # )
        # self._test_merge(salmon_dataset, salmon_dataset2.repro_tag)

        assert self.test_dataset[0] == self.test_dataset[len(self.test_dataset)]
        assert self.test_dataset[0] != self.test_dataset[len(self.test_dataset) - 1]

    def _test_store(self, org_name: str, dataset_name: str):
        datasets_dir = Path(self.server_config["test_dataset_storage_dir"])
        kd_builder = KDBuilder(root=datasets_dir, name=dataset_name)
        kd_builder.add_dir_annotation(location=Path("salmon_train"))
        kd_builder.add_dir_annotation(location=Path("salmon_val"))
        kd_builder.add_dir_annotation(location=Path("salmon_test"))

        # TODO: this doesn't give helpful errors when trying to store under an invalid org name.
        salmon_dataset = KnapsackDataset(name="salmon", org_name=self.org_name)
        salmon_dataset.from_kd_builder(kd_builder)
        salmon_repro_tag = salmon_dataset.store()
        salmon_dataset_size = len(salmon_dataset)
        print(f"_test_store - size of salmon_dataset {salmon_dataset_size} \n "
              f"--- repro_tag: {salmon_repro_tag}")

        return salmon_dataset

    def _test_procure(self, dataset_name: str) -> KnapsackDataset:
        salmon_dataset = KnapsackDataset(name=dataset_name, org_name=self.org_name)
        salmon_dataset.procure()
        salmon_dataset_size = len(salmon_dataset)
        print(f"_test_procure - size of procured salmon_dataset: {salmon_dataset_size}"
              f" --- repro_tag: {salmon_dataset.repro_tag}")
        return salmon_dataset

    def _test_append(
        self,
        ks_dataset: KnapsackDataset,
        dataset_name: str
    ) -> None:
        datasets_dir = Path(self.server_config["test_dataset_storage_dir"])
        kd_builder = KDBuilder(root=datasets_dir, name=dataset_name)
        kd_builder.add_dir_annotation(location=Path("salmon_append1"))
        ks_dataset.append(kd_builder)
        ks_dataset_size = len(ks_dataset)
        print(
            "_test_append - " +
            f"size of appended dataset: {ks_dataset_size}" +
            f"--- repro_tag: {ks_dataset.repro_tag}"
        )

    def _test_merge(self, dataset: KnapsackDataset, other_repro_tag: str):
        starting_repro_tag = dataset.starting_repro_tag
        dataset.merge(other_repro_tag, use_existing_dataset_name=True)
        assert starting_repro_tag != dataset.repro_tag
        assert starting_repro_tag != other_repro_tag
        # TODO: assert that both repro_tags are in the version history of
        # the newly merged dataset.
        dataset_size = len(dataset)
        print(f"_test_merge - size of merged salmon_dataset: {dataset_size}"
              f"--- repro_tag: {dataset.repro_tag}")
        return dataset

    def _get_list_of_all_filenames_in_dir(self, root_dir: Path) -> List[str]:
        result = []
        for root, dirs, files in os.walk(str(root_dir)):
            for file in files:
                result.append(Path(file).name)
        return result

    def _remove_all_files_in_local_knapsack(self):
        for root, dirs, files in os.walk(str(self.LOCAL_KNAPSACK_STORAGE_LOCATION)):
            for file in files:
                full_file = os.path.join(root, file)
                print("REMOVING: ", full_file)
                os.remove(full_file)

    def _remove_all_files_in_remote_knapsack(self):
        for root, dirs, files in os.walk(str(self.REMOTE_KNAPSACK_STORAGE_LOCATION)):
            for file in files:
                full_file = os.path.join(root, file)
                print("REMOVING: ", full_file)
                # os.remove(full_file)
