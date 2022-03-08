# 
# Simple check on the number of arguments, we always expect 5 args. 
# One for each service URL, and the last argument whether a file should be saved
#

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

# Some helper function that writes the metadata from the output JSON.
write_metadata () {
    echo "Finished $1 the data. version: $(echo $2 | jq .version), datetime: $(echo $2 | jq .datetime)"
}

# If a command errors, we want to exit the program to prevent an errornuous continuation of the program
exit_on_error () {
    if [ $1 == 1 ]; then
        echo "Program errored, exiting pipeline..."
        exit 1
    fi
}

## PREPROCESSING STEPS
# 1.) Passes the data to the preprocessing URL
echo "Start preprocessing the data..."
PREPROCESSED=$(cat data/train_input.json | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$PREPROCESSOR_SERVICE/preprocess)
exit_on_error $?
echo
# 2.) Write the metadata from the response
write_metadata "PREPROCESSING" $PREPROCESSED
echo

## SPLITTING STEPS
# 1.) Pass the 'out' value from the $PREPROCESSED dict to the splitter URL
echo "Start splitting the data..."
SPLITTED=$(echo $PREPROCESSED | jq .out | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$SPLITTER_SERVICE/split)
exit_on_error $?

# 2.) Save the created training & testing data split in memory
TRAIN_DATA=$(echo $SPLITTED | jq .out.train)
TEST_DATA=$(echo $SPLITTED | jq .out.test)
echo

# 3.) Write the metadata from the response
write_metadata "SPLITTING" $SPLITTED
echo

## TRAINING STEPS
# 1.) Pass the temporarily saved $TRAIN_DATA to the trainer URL
echo "Start training the using the training data..."
TRAINED=$(echo $TRAIN_DATA | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$TRAINER_SERVICE/train)
exit_on_error $?

# 2.) Save the cross-validation results and the trained model in memory
CV_RESULT=$(echo $TRAINED | jq .out.cv_result)
MODEL=$(echo $TRAINED | jq .out.model)
echo

# 3.) Write the metadata from the response
write_metadata "TRAINING" $TRAINED
echo

## VALIDATION STEPS
# 1.) Pass the temporarily saved $MODEL and $TEST_DATA to the validator URL 
echo "Start validating using the test data, and model..."
VALIDATION=$(echo "{\"model\": $MODEL, \"test_data\": $TEST_DATA}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$VALIDATOR_SERVICE/validate)
exit_on_error $?

# 2.) Retrieve the metrics computed and responded from the validator.
METRICS_DICT=$(echo $VALIDATION | jq .out.metrics_dict)
write_metadata "VALIDATING" $VALIDATION
echo
echo "We have finished: Preprocessing, Splitting, Training & validating the model. The resulting validation scores:"
echo $METRICS_DICT | jq .

## SAVING
# If the scripts was asked to save the model...
# 1. Compute the hash-name of the model by computing a hash over the used model
# 2. If the models folder does not yet exist, create it
# 3. Save the model to the 'models/' folder
if [ $save_model == 1 ]; then
    MODEL_NAME=$(echo $VALIDATION | jq .out.model | sha1sum | awk '{print $1}')

    mkdir -p models

    echo "Saving model to 'models/$MODEL_NAME.json'"
    echo "{\"model_data\": $VALIDATION, \"test_data\": $TEST_DATA, \"train_data\": $TRAIN_DATA}" > models/$MODEL_NAME.json
fi
