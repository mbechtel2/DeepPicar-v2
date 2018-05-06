#sudo service lightdm stop
for f in /sys/devices/system/cpu/cpu?; do
	echo "performance" > $f/cpufreq/scaling_governor
	#echo 600000 > $f/cpufreq/scaling_setspeed
done
