MODEL_FILEPATH=$1

if [ -z $MODEL_FILEPATH ]; then
    echo "Please provide a models file. Exiting..."
    exit 1
fi

. .venv/bin/activate
python3 -m tools.show_plot $MODEL_FILEPATH
deactivate
