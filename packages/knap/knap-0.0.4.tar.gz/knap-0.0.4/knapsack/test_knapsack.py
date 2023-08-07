from pathlib import Path

from knapsack.knapsack_dataset import KnapsackDataset
from knapsack.kd_builder import KDBuilder, Split


if __name__ == "__main__":
    lvis_v1_root = '/home/ubuntu/crucible/datasets/lvis-v1'
    lvis_kd_builder = KDBuilder(root=lvis_v1_root, name='lvis-v1')
    lvis_kd_builder.add_dir_annotation(
        location=Path('train2017/train2017'),
        split=Split.TRAIN,
    )
    lvis_kd_builder.add_dir_annotation(
        location=Path('lvis_v1_val/val2017'),
        split=Split.VAL,
    )
    lvis_kd_builder.add_dir_annotation(
        location=Path('lvis_v1_test/test2017'),
        split=Split.TEST,
    )

    lvis_kd_builder.add_coco_style_annotation_file(
        Path('lvis_v1_train.json/lvis_v1_train.json'),
        split=Split.TRAIN
    )
    lvis_kd_builder.add_coco_style_annotation_file(
        Path('lvis_v1_val/lvis_v1_val.json'),
        split=Split.VAL
    )
    lvis_kd_builder.add_coco_style_annotation_file(
        Path('lvis_v1_test/lvis_v1_image_info_test_challenge.json'),
        split=Split.TEST
    )

    lvis = KnapsackDataset(name='lvis_v1')
    lvis.load_from_local_fs(lvis_kd_builder)

    repro_tag = lvis.store()

    lvis.procure(repro_tag=repro_tag)
