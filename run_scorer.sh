MODEL_NAME=$1
BALANCE_HISTORY=$2

MODEL=$(cat models/$MODEL_NAME.json | jq .model_data.out.model)
TEST_DATA=$(cat models/$MODEL_NAME.json | jq .test_data)
TEST_DATA=$(cat data/invalid_test_data.json)

SCORER=$(echo "{\"model\": $MODEL, \"balance_history\": $TEST_DATA}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://localhost:8004/score)
echo $SCORER
