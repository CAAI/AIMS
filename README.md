# AIMS
Automatic MS lesion delineation model. nnU-Net trained on 549 clinical patientients

# AIMS
Automatic delineation of MS lesions. The model, a nnU-Net, was trained on 549 clinical patients.

Please cite for use:

Hindsholm AM, Andersen FL, Cramer SP, Simonsen HJ, Askløf MG, Magyari M, Madsen PN, Hansen AE, Sellebjerg F, Larsson HBW, Langkilde AR, Frederiksen JL, Højgaard L, Ladefoged CN and Lindberg U (2023) Scanner agnostic large-scale evaluation of MS lesion delineation tool for clinical MRI. Front. Neurosci. 17:1177540. doi: 10.3389/fnins.2023.1177540

## Usage:
The models require FLAIR, T2, and T1 input files. You can call the function with:

`AIMS -flair <FLAIR.nii.gz> -t2 <T2.nii.gz> -t1 <T1.nii.gz> -o <AIMS_mask.nii.gz>`

You can also run the function on a folder with preprocessed and correctly formatted files:
`AIMS_folder -input <INPUT_FOLDER> -o <OUTPUT_FOLDER>`

The files in the folder must be named `<PatientID>_0000.nii.gz` (the flair), `<PatientID>_0001.nii.gz` (the t2), `<PatientID>_0002.nii.gz` (the t1). The output dir will contain the file `<PatientID>.nii.gz` (the output mask), for each PatientID. AIMS_folder is much faster than AIMS when you need to process many files. AIMS_folder require already preprocessed files (see below).

### Preprocessing

Before you run the above command, you first need to perform the following preprocessing steps:
- Standard orientation with `reorient2std`, 
- Resample to same spacing (e.g. FLAIR) with `flirt`
- Skull strip, e.g. with `hd-bet`

If you wish to perform these steps as part of the algorithm, call the function with the `--preprocess` flag:

`AIMS -flair <FLAIR.nii.gz> -t2 <T2.nii.gz> -t1 <T1.nii.gz> -o <AIMS_mask.nii.gz> --preprocess`

