for f in /sys/devices/system/cpu/cpu?; do
	echo "performance" > $f/cpufreq/scaling_governor
done
