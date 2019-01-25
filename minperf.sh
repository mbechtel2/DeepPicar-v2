for f in /sys/devices/system/cpu/cpu?; do
	echo "powersave" > $f/cpufreq/scaling_governor
done
