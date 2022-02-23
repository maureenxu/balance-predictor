min_nof_args=5
if [ $# -ne $min_nof_args ]; then
    echo "Illegal number of arguments";
    exit 1
fi

PREPROCESSOR_SERVICE=$1
SPLITTER_SERVICE=$2
TRAINER_SERVICE=$3
VALIDATOR_SERVICE=$4
save_model=$5

echo "Service URL's: $PREPROCESSOR_SERVICE, $SPLITTER_SERVICE, $TRAINER_SERVICE, $VALIDATOR_SERVICE"

shift $((OPTIND-1))

[ "${1:-}" = "--" ] && shift


write_metadata () {
    echo "Finished $1 the data. version: $(echo $2 | jq .version), datetime: $(echo $2 | jq .datetime)"
}

exit_on_error () {
    if [ $1 == 1 ]; then
        echo "Program errored, exiting pipeline..."
        exit 1
    fi
}

echo "Start preprocessing the data..."
PREPROCESSED=$(cat data/input.json | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$PREPROCESSOR_SERVICE/preprocess)
exit_on_error $?
echo
write_metadata "PREPROCESSING" $PREPROCESSED
echo
echo "Start splitting the data..."
SPLITTED=$(echo $PREPROCESSED | jq .out | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$SPLITTER_SERVICE/split)
exit_on_error $?

TRAIN_DATA=$(echo $SPLITTED | jq .out.train)
TEST_DATA=$(echo $SPLITTED | jq .out.test)
echo
write_metadata "SPLITTING" $SPLITTED
echo
echo "Start training the using the training data..."
TRAINED=$(echo $TRAIN_DATA | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$TRAINER_SERVICE/train)
exit_on_error $?

CV_RESULT=$(echo $TRAINED | jq .out.cv_result)
MODEL=$(echo $TRAINED | jq .out.model)
echo
write_metadata "TRAINING" $TRAINED
echo
echo "Start validating using the test data, and model..."
VALIDATION=$(echo "{\"model\": $MODEL, \"test_data\": $TEST_DATA}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$VALIDATOR_SERVICE/validate)
exit_on_error $?

METRICS_DICT=$(echo $VALIDATION | jq .out.metrics_dict)
write_metadata "VALIDATING" $VALIDATION
echo
echo "We have finished: Preprocessing, Splitting, Training & validating the model. The resulting validation scores:"
echo $METRICS_DICT | jq .


if [ $save_model == 1 ]; then
    MODEL_NAME=$(echo $VALIDATION | jq .out.model | sha1sum | awk '{print $1}')
    MODEL_DATETIME=$(echo $VALIDATION | jq .datetime)
    MODEL_VERSION=$(echo $VALIDATION | jq .version)

    mkdir -p models

    echo "Saving model to 'models/$MODEL_NAME.json'"
    echo "{\"model_data\": $VALIDATION, \"test_data\": $TEST_DATA, \"train_data\": $TRAIN_DATA}" > models/$MODEL_NAME.json
fi
