from nnunet.inference.predict import predict_cases, predict_from_folder
from AIMS.paths import folder_with_parameter_files
from AIMS.utils import maybe_download_parameters
import os

def run_AIMS(MRIs, output_file, model_checkpoint_name):
    
    for i in range(4):
        maybe_download_parameters(model_checkpoint_name, i)

    model_dir = os.path.join(folder_with_parameter_files, model_checkpoint_name)
    predict_cases(model_dir, [MRIs], [output_file], (0, ), False, 1, 1, None, True,
                  None, True)
    
def run_AIMS_from_folder(input_folder, output_folder, model_checkpoint_name, processes=4, overwrite_existing=True):
    
    for i in range(4):
        maybe_download_parameters(model_checkpoint_name, i)

    model_dir = os.path.join(folder_with_parameter_files, model_checkpoint_name)
    predict_from_folder(model_dir, input_folder, output_folder, (0, ), False, processes, processes,
                        None, 0, 1, True, overwrite_existing=overwrite_existing)