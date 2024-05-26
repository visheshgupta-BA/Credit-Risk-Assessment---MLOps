import os
import pickle
import pandas as pd
import logging

# Configure logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(PROJECT_DIR, 'logs', 'datapipeline.log')
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)  # Ensure the directory exists
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(LOG_PATH)

INPUT_PICKLE_PATH = os.path.join(PROJECT_DIR, 'data', 'processed','after_year.pkl')
OUTPUT_PICKLE_PATH = os.path.join(PROJECT_DIR, 'data', 'processed','after_dummies.pkl')

def get_dummies(input_pickle_path=INPUT_PICKLE_PATH,
                            output_pickle_path=OUTPUT_PICKLE_PATH):
    """
    -----
    Function: get_dummies
    
    Description:
    This function loads a pandas DataFrame from a specified pickle file, applies one-hot encoding to categorical columns, and saves the modified DataFrame back to a pickle file. If the input file path does not exist, it logs an error and raises FileNotFoundError.
    
    Parameters:
    - input_pickle_path (str): Path to the input pickle file containing the DataFrame. Default is INPUT_PICKLE_PATH.
    - output_pickle_path (str): Path to save the modified DataFrame as a pickle file. Default is OUTPUT_PICKLE_PATH.
    
    Returns:
    str: Path to the saved pickle file containing the modified DataFrame.
    -----
    """
    logger.info(">>>>>>>>>>>>>>>>>>>>>> Started Get Dummies Task <<<<<<<<<<<<<<<<<<<<<<<<<<<")

    if os.path.exists(input_pickle_path):
        with open(input_pickle_path, "rb") as file:
            df = pickle.load(file)
    else:
        error_message = f"No data found at the specified path: {input_pickle_path}"
        logger.error(error_message)
        raise FileNotFoundError(error_message)

    df=pd.get_dummies(df,columns=['grade', 'verification_status', 'purpose', 'initial_list_status',
           'application_type', 'home_ownership'],dtype=int)
    
    logger.info(">>>>>>>>>>>>>>>>>>>>>> Get Dummies Task Completed <<<<<<<<<<<<<<<<<<<<<<<<<<<")

    with open(output_pickle_path, "wb") as file:
        pickle.dump(df, file)
    logger.info(f"Data saved to {output_pickle_path}.")
    return output_pickle_path
