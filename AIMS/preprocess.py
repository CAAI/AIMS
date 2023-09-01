#!/usr/bin/env python3

import numpy as np
import os
import subprocess as subp
import multiprocessing as mp
from functools import partial
import nibabel as nib
from AIMS.utils import maybe_mkdir_p
import shutil


def reorient2std(file_, overwrite=False):
    out_file = file_.replace(".nii.gz", "_r2s.nii.gz")
    if not os.path.exists(out_file) or overwrite:
        cmd = ["fslreorient2std", file_, out_file]
        output = subp.check_output(cmd)
    else:
        output = "{} already exists and overwrite=False.".format(out_file)
    return out_file, output


def register(file_, reference_file, overwrite=False):
    out_file = file_.replace(".nii.gz", "_reg.nii.gz")
    mat_file = file_.replace(".nii.gz", "_reg.mat")
    if not os.path.exists(out_file) or overwrite:
        cmd = [
            "flirt",
            "-in",
            file_,
            "-ref",
            reference_file,
            "-out",
            out_file,
            "-dof",
            "6",
            "-interp",
            "spline",
            "-omat",
            mat_file,
        ]
        output = subp.check_output(cmd)
    else:
        output = "{} already exists and overwrite=False.".format(out_file)
    return out_file, output

""" FUNCTION INSPIRED BY https://github.com/NeuroAI-HD/HD-GLIO-AUTO/blob/master/scripts/run.py """
def preprocess(files, verbose=False, overwrite=False):
    names = ["FLAIR", "T2", "T1"] if len(files) == 3 else ["FLAIR", "T2"]
    output_dir = os.path.dirname(files[0])
    if output_dir=='':
        output_dir = '.'
    existing_files = os.listdir(output_dir)

    # Reorient to standard
    p = mp.Pool(min(len(files), mp.cpu_count()))
    results = p.map(partial(reorient2std, overwrite=overwrite), files)
    files, outputs = list(zip(*results))
    files = list(files)
    if verbose:
        print(
            "Reoriented all files to standard orientation with the following outputs:"
        )
        for output in outputs:
            print(output)

    # save the current files, we will use the transformations from
    # the registrations AFTER BET to register them to a reference space
    # and then apply the BET mask!
    files_r2s = [f for f in files]

    # check the spacing for all files to determine which one will be our
    # reference. Default is T1
    ref_index = 0
    min_spacing = 1e9
    for f, file_ in enumerate(files):
        try:
            file_ = nib.load(file_)
            spacing = float(np.product(file_.header.get_zooms()))
            if spacing < min_spacing:
                min_spacing = spacing
                ref_index = f
        except Exception as e:
            continue
    if verbose:
        print("Using contrast {} as reference".format(names[ref_index]))

    # Brain extraction (do not parallelize because we run on gpu)
    mask_files = []
    for f, file_ in enumerate(files):
        mask_file = file_.replace(".nii.gz", "_bet_mask.nii.gz")
        mask_files.append(mask_file)
        new_file = file_.replace(".nii.gz", "_bet.nii.gz")
        if (
            not overwrite
            and os.path.basename(new_file) in existing_files
            and os.path.basename(mask_file) in existing_files
        ):
            files[f] = new_file
            print(
                "{} and {} already exist, continuing.".format(
                    os.path.basename(new_file), os.path.basename(mask_file)
                )
            )
            continue

        subp.check_output(["hd-bet", "-i", file_, "-device", "0"])

        cmd = ["fslmaths", new_file, "-mas", mask_file, new_file]
        output2 = subp.check_output(cmd)
        files[f] = new_file
        if verbose:
            print(
                "Applied brain extraction for {} with the following output:".format(
                    os.path.basename(file_)
                )
            )
            print(output)

    # Register to reference
    results = p.map(
        partial(
            register, reference_file=files[ref_index], overwrite=overwrite
        ),
        files,
    )
    files, outputs = list(zip(*results))
    if verbose:
        print("Registered all sequences to reference with the following outputs:")
        for output in outputs:
            print(output)

    # Transform original files (after r2s) to reference space with .mat files
    # from previous step, then apply reference BET mask.
    for f, file_ in enumerate(files_r2s):
        name = files[f]
        ref_file = files[ref_index]
        mat_file = files[f].replace(".nii.gz", ".mat")
        mask_file = mask_files[ref_index]  # reference BET mask
        cmd = [
            "flirt",
            "-in",
            file_,
            "-out",
            name,
            "-ref",
            ref_file,
            "-applyxfm",
            "-init",
            mat_file,
            "-interp",
            "spline",
        ]
        output = subp.check_output(cmd)
        cmd = ["fslmaths", name, "-mas", mask_file, name]
        output2 = subp.check_output(cmd)
        if verbose:
            print("Re-applied masks to registered files with outputs:")
            print(output)
            print(output2)
    

    if verbose:
        print("Done with preprocessing. The final output files are:", ', '.join(files))

    return files