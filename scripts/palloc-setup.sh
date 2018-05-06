#Enable bits 12, 13, and 14
echo 0x00006000 > /sys/kernel/debug/palloc/palloc_mask

#Create 4 partitions
cgcreate -g palloc:part1
cgcreate -g palloc:part2
cgcreate -g palloc:part3
cgcreate -g palloc:part4
cgcreate -g palloc:part5
cgcreate -g palloc:part6
cgcreate -g palloc:part7
cgcreate -g palloc:part8

#Assign bins to partitions
echo 0 > /sys/fs/cgroup/palloc/part1/palloc.bins #Multimodel 4Nx1C and Bandwidth
echo 1 > /sys/fs/cgroup/palloc/part2/palloc.bins
echo 2 > /sys/fs/cgroup/palloc/part3/palloc.bins
echo 3 > /sys/fs/cgroup/palloc/part4/palloc.bins
echo 0-1 > /sys/fs/cgroup/palloc/part5/palloc.bins #Multimodel 2Nx2C
echo 2-3 > /sys/fs/cgroup/palloc/part6/palloc.bins
echo 0-2 > /sys/fs/cgroup/palloc/part7/palloc.bins #Multicore 3c
echo 0-3 > /sys/fs/cgroup/palloc/part8/palloc.bins #Multicore 4c


#Enable PALLOC 
echo 1 > /sys/kernel/debug/palloc/use_palloc