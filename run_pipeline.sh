
PREPROCESSED=$(cat data/input.json | curl -H "Content-Type: application/json" -X POST -d @- http://127.0.0.1:8000/preprocess)
SPLITTED=$(echo $PREPROCESSED | curl -H "Content-Type: application/json" -X POST -d @- http://localhost:8001/split)
TRAIN_DATA=$(echo $SPLITTED | jq .train)
TEST_DATA=$(echo $SPLITTED | jq .test)

TRAINED=$(echo $TRAIN_DATA | curl -H "Content-Type: application/json" -X POST -d @- http://localhost:8002/train)
CV_RESULT=$(echo $TRAINED | jq .cv_result)
MODEL=$(echo $TRAINED | jq .model)

VALIDATION=$(echo "{\"model\": $MODEL, \"test_data\": $TEST_DATA}" | curl -H "Content-Type: application/json" -X POST -d @- http://localhost:8003/validate)
echo $VALIDATION
