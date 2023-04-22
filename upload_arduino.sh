sleep 1

echo Compiling $2 &&
arduino-cli compile --fqbn arduino:avr:uno $2 &&

echo Uploading $2 on $1 &&
arduino-cli upload -p $1 --fqbn arduino:avr:uno $2 &&
echo Uploaded &&

sleep 0.5