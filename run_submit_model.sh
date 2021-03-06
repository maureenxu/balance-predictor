# SERVER_ADDRESS=api.some.remote.server.com
SERVER_ADDRESS=localhost:8004


MODEL_NAME=$1
MODEL=$(cat models/$MODEL_NAME.json | jq .model_data.out.model)

# Submit the model to the scorer endpoint 
SCORER=$(echo "{\"model\": $MODEL}" | curl --show-error --fail -s -H "Content-Type: application/json" -X POST -d @- http://$SERVER_ADDRESS/submit)
if [ $? == 1 ]; then
    echo 'Submission failed'
    exit 1
fi
