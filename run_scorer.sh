MODEL_NAME=$1
DATA_FILEPATH=$2

MODEL=$(cat models/$MODEL_NAME.json | jq .model_data.out.model)
DATA_TO_SCORE=$(cat $DATA_FILEPATH)

SCORER=$(echo "{\"model\": $MODEL, \"balance_history\": $DATA_TO_SCORE}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://localhost:8004/score)
echo $SCORER
