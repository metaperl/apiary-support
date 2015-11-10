#!/bin/bash -x


CRUN=$HOME/prg/apiary-support/fttf/cron/crun
FTTF=$HOME/prg/apiary-support/fttf
INSTRUMENTS=EUR_USD,GBP_USD,AUD_USD,USD_JPY,USD_CAD,USD_CHF,NZD_USD
OPTS="--trade --save-graph"


$CRUN "cd $FTTF ; ./main.py $OPTS --instruments=$INSTRUMENTS --timeframes=W"
$CRUN "cd $FTTF ; ./main.py $OPTS --instruments=$INSTRUMENTS --timeframes=M"
