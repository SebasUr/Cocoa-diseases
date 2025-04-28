#!/usr/bin/env python3
"""
Script to reorganize a YOLO dataset by copying/moving images and labels
from `train/`, `valid/`, `test/` into a mirrored structure in the output directory:

output_dir/
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/

Each subset has its own counter (e.g., 000001.jpg/.txt, ...).
Errors are printed only when a label file is missing.
"""
import os
import shutil
import argparse

def process_subset(subset, src_root, dst_root, keep):
    images_src = os.path.join(src_root, subset, 'images')
    labels_src = os.path.join(src_root, subset, 'labels')
    images_dst = os.path.join(dst_root, subset, 'images')
    labels_dst = os.path.join(dst_root, subset, 'labels')

    if not os.path.isdir(images_src):
        print(f"[WARNING] {images_src} not found, skipping subset '{subset}'")
        return 0

    os.makedirs(images_dst, exist_ok=True)
    os.makedirs(labels_dst, exist_ok=True)

    counter = 1
    for fname in sorted(os.listdir(images_src)):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        base, ext = os.path.splitext(fname)
        src_img = os.path.join(images_src, fname)
        src_lbl = os.path.join(labels_src, base + '.txt')

        new_name = f"{counter:06d}"
        dst_img = os.path.join(images_dst, new_name + ext)
        dst_lbl = os.path.join(labels_dst, new_name + '.txt')

        # Move or copy image
        if keep:
            shutil.copy2(src_img, dst_img)
        else:
            shutil.move(src_img, dst_img)

        # Move/copy label or create empty + error
        if os.path.exists(src_lbl):
            if keep:
                shutil.copy2(src_lbl, dst_lbl)
            else:
                shutil.move(src_lbl, dst_lbl)
        else:
            open(dst_lbl, 'a').close()
            print(f"[ERROR] Label not found for image {subset}/{fname}; created empty {subset}/{new_name}.txt")

        counter += 1

    return counter - 1

def main():
    parser = argparse.ArgumentParser(
        description='Reorganize YOLO dataset preserving train/valid/test structure.'
    )
    parser.add_argument('--input_dir', default='.', help='Root dir with train/, valid/, test/')
    parser.add_argument('--output_dir', default='output', help='Destination root dir')
    parser.add_argument('--subsets', nargs='+', default=['train','valid','test'],
                        help='Which subsets to process')
    parser.add_argument('--keep', action='store_true', help='Copy files instead of moving')
    args = parser.parse_args()

    total = 0
    for subset in args.subsets:
        processed = process_subset(subset, args.input_dir, args.output_dir, args.keep)
        if processed:
            print(f"[{subset}] {processed} files processed.")
        total += processed

    print(f"Done! Total images processed across subsets: {total}")

if __name__ == '__main__':
    main()
