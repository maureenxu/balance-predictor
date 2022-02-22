# SERVER_ADDRESS=score.api.thereisawebsiteforeverything.com
SERVER_ADDRESS=localhost:8004

DATA_FILEPATH=$1
MODEL_NAME=$2

DATA_TO_SCORE=$(cat $DATA_FILEPATH)

if [ -z "$MODEL_NAME" ]; then
    SCORER=$(echo "{\"balance_history\": $DATA_TO_SCORE}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$SERVER_ADDRESS/score)
    echo $SCORER
else
    MODEL=$(cat models/$MODEL_NAME.json | jq .model_data.out.model)
    SCORER=$(echo "{\"model\": $MODEL, \"balance_history\": $DATA_TO_SCORE}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$SERVER_ADDRESS/score)
    echo $SCORER
fi

