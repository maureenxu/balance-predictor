import argparse
import os
import pickle

from src import split, utils
import src.configuration as config

app = FastAPI()


@app.get('/start_splitting')
async def split(request: Request):
    input_path = os.path.join(args.input_path, config.INPUT_OUTPUT_FILENAMES["spliter"]["input"])

    with open(input_path, "rb") as input_file:
        df = pickle.load(input_file)

    spliter = split.DataSpliter(df, args.split_ratio)
    df_train, df_test = spliter.split()

    utils.pickle_dump_output(args.output_train_path, config.INPUT_OUTPUT_FILENAMES["spliter"]["output_train"], df_train)
    utils.pickle_dump_output(args.output_test_path, config.INPUT_OUTPUT_FILENAMES["spliter"]["output_test"], df_test)

    requests.get('trainer.localhost:8010/start_training')
    return Response(200)
