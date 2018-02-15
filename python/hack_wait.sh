#!/usr/bin/env bash

cmd="$@"

function postgres_ready(){
python << END
import sys
sys.exit(-1)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

exec $cmd