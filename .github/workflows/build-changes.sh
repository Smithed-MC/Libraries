BROADCAST=()
for PACK in $(ls smithed_libraries/packs); do
  # Get the pack's version number
  PACK_VERSION=$(cat smithed_libraries/packs/${PACK}/beet.yaml | grep "version:" | cut -d ":" -f 2)
  PACK_VERSION=$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<< "$PACK_VERSION")  # strip whitespace

  OLD_PACK_VERSION=$(git show HEAD~1:smithed_libraries/packs/${PACK}/beet.yaml | grep "version:" | cut -d ":" -f 2)
  OLD_PACK_VERSION=$(sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' <<< "$OLD_PACK_VERSION")   # strip whitespace

  # Check if the pack's version number has changed
  if [ "$PACK_VERSION" != $OLD_PACK_VERSION ]; then
    BROADCAST+=("-s broadcast[] = smithed_libraries/packs/$PACK")
  fi
done

# Build the packs (if there are any to build)
if [ -n "$BROADCAST" ]; then
  beet --log INFO -p beet-release.yaml "${BROADCAST[@]}"
else
  exit 1  # error to kill the rest of the steps
fi
