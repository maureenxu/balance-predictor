
# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
save_model=0

while getopts "h?s" opt; do
  case "$opt" in
    h|\?)
      show_help
      exit 0
      ;;
    s)  save_model=1
      ;;
  esac
done

./run_pipeline.sh localhost:8000 localhost:8001 localhost:8002 localhost:8003 $save_model