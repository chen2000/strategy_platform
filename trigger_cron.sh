# use for cron job in server
export STRATEGY_PATH=/home/bigmii/strategy_platform/
export PYTHONPATH=$PYTHONPATH:STRATEGY_PATH
cd /home/bigmii/strategy_platform/
. env/bin/activate
echo 'start running' >> cronlog.txt
python workflows/test_dow30.py
