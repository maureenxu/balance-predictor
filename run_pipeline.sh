SHOW_PLOT=${1:-true}

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
PREPROCESSED=$(cat data/input.json | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://localhost:8000/preprocess)
exit_on_error $?
echo
write_metadata "PREPROCESSING" $PREPROCESSED
echo
echo "Start splitting the data..."
SPLITTED=$(echo $PREPROCESSED | jq .out | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://localhost:8001/split)
exit_on_error $?

TRAIN_DATA=$(echo $SPLITTED | jq .out.train)
TEST_DATA=$(echo $SPLITTED | jq .out.test)
echo
write_metadata "SPLITTING" $SPLITTED
echo
echo "Start training the using the training data..."
TRAINED=$(echo $TRAIN_DATA | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://localhost:8002/train)
exit_on_error $?

CV_RESULT=$(echo $TRAINED | jq .out.cv_result)
MODEL=$(echo $TRAINED | jq .out.model)
echo
write_metadata "TRAINING" $TRAINED
echo
echo "Start validating using the test data, and model..."
VALIDATION=$(echo "{\"model\": $MODEL, \"test_data\": $TEST_DATA}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://localhost:8003/validate?show_plot=$SHOW_PLOT)
exit_on_error $?

METRICS_DICT=$(echo $VALIDATION | jq .out.metrics_dict)
write_metadata "VALIDATING" $VALIDATION
echo
echo "We have finished: Preprocessing, Splitting, Training & validating the model. The resulting validation scores:"
echo $METRICS_DICT | jq .
