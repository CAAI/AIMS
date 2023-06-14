from urllib.request import urlopen
import os, sys
from AIMS.paths import folder_with_parameter_files

def download(ID, fold, out_dir):
    for suffix in ['.model','.model.pkl']:
        url = f"https://zenodo.org/record/{ID}/files/{fold}{suffix}?download=1"

        print("Downloading", url, "...")
        data = urlopen(url).read()
        with open(os.path.join(out_dir, f'model_best{suffix}'), 'wb') as f:
            f.write(data)

    # Also download plans
    if fold==0:
        url = f"https://zenodo.org/record/{ID}/files/plans.pkl?download=1"
        print("Downloading", url, "...")
        data = urlopen(url).read()
        with open(os.path.join(out_dir, '..', 'plans.pkl'), 'wb') as f:
            f.write(data)
        

def download_parameters_FLAIR_T2_T1_orig_model(fold, out_dir):
    ID = '8037554'
    download(ID, fold, out_dir)
        

def maybe_download_parameters(model_name='FLAIR_T2_T1_orig', fold=0, force_overwrite=False):
    """
    Downloads the parameters for some fold if it is not present yet.
    :param fold:
    :param force_overwrite: if True the old parameter file will be deleted (if present) prior to download
    :return:
    """
    trained_models = {
        'FLAIR_T2_T1_orig': download_parameters_FLAIR_T2_T1_orig_model,
    }

    assert 0 <= fold <= 3, "fold must be between 0 and 3"
    assert model_name in trained_models, "selected model is not available"

    model_folder_with_parameter_files = os.path.join(folder_with_parameter_files, model_name, f'fold_{fold}')

    if not os.path.isdir(model_folder_with_parameter_files):
        maybe_mkdir_p(model_folder_with_parameter_files)

    if force_overwrite and os.path.isfile(os.path.join(model_folder_with_parameter_files, 'model_best.model')):
        os.remove(os.path.join(model_folder_with_parameter_files, 'model_best.model'))
        os.remove(os.path.join(model_folder_with_parameter_files, 'model_best.model.pkl'))
        os.remove(os.path.join(folder_with_parameter_files, model_name, 'plans.pkl'))
    if not os.path.isfile(os.path.join(model_folder_with_parameter_files, 'model_best.model')):
        trained_models[model_name](fold, model_folder_with_parameter_files)


def maybe_mkdir_p(directory):
    splits = directory.split("/")[1:]
    for i in range(0, len(splits)):
        if not os.path.isdir(os.path.join("/", *splits[:i+1])):
            os.mkdir(os.path.join("/", *splits[:i+1]))


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__