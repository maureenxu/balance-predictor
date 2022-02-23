SERVER_ADDRESS=api.thereisawebsiteforeverything.com

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

./run_pipeline.sh preprocess.$SERVER_ADDRESS split.$SERVER_ADDRESS train.$SERVER_ADDRESS validate.$SERVER_ADDRESS $save_model
