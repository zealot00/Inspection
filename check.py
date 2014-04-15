#! /usr/bin/env python
#coding:utf-8

import subprocess
import time
import platform
import psutil


class PSU(object):

    def __init__(self):
       self.warning_repo = ""

    def getCpuStatus(self):
        cpustatus = {}
        cpustatus['cpustat'] = psutil.cpu_percent(interval=int(psutil.NUM_CPUS))
        return cpustatus

    def getMemStatus(self):
        memstatus = {}
        memstatus['total_phymem'] = str(int(psutil.TOTAL_PHYMEM ) /1024 /1024) + " MB"
        memstatus['total_virtmem'] = str(int(psutil.total_virtmem()) /1024 /1024) + " MB"
        memstatus['phymem_usage_percent'] = psutil.phymem_usage().percent
        memstatus['phymem_usage_used'] = str(int(psutil.phymem_usage().used) /1024 /1024) + "MB"
        memstatus['phtmem_usage_free'] = str(int(psutil.phymem_usage().free) /1024 /1024) + "MB"
        memstatus['virtmem_usage_percent'] = psutil.virtmem_usage().percent
        memstatus['virtmem_usage_used'] = str(int(psutil.virtmem_usage().used) /1024 /1024) + "MB"
        memstatus['virtmem_usage_free'] = str(int(psutil.virtmem_usage().free) /1024 /1024) + "MB"
        return memstatus

    def getDiskStatus(self):
        diskstatus = {}
        get_sys_disk_partitions_list = []

        for get_sys_disk_partitions_info in psutil.disk_partitions():
            get_sys_disk_partitions_list.append(get_sys_disk_partitions_info.mountpoint)

        get_sys_disk_usage_list = []

        for get_sys_disk_partitions in get_sys_disk_partitions_list:
            disk_usage = psutil.disk_usage(get_sys_disk_partitions)
            get_sys_disk_usage_list.append([str(int(disk_usage.total) /1000 /1000 ) + "MB",str(int(disk_usage.used) /1000 /1000) + "MB" ,str(int(disk_usage.free) /1000 /1000) + "MB" ,str(disk_usage.percent) + "%"])

        diskstatus = dict(zip(get_sys_disk_partitions_list,get_sys_disk_usage_list))

        return diskstatus

            
         





def getNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())



def getSystemInfo():
#   这里返回的是一个字典，字典的index内容分别是系统类型，本地的默认计算机名称，内核版本,发行版本,python版本
    systeminfo = {}
    systeminfo['system'] = platform.uname()[0]
    systeminfo['hostname'] = platform.uname()[1]
    systeminfo['kernel'] = platform.uname()[2]
    systeminfo['release'] = platform.linux_distribution()[0] + platform.linux_distribution()[1]
    systeminfo['python-version'] = platform.python_version()
    
    return systeminfo


def getSystemLoad():
    loadavg = {}
    f = open("/proc/loadavg")
    con = f.read().split()
    f.close()
    loadavg['load_1'] = con[0]
    loadavg['load_5'] = con[1]
    loadavg['load_15'] = con[2]

    return loadavg



def getPerformanceParameters():
#这里会显示系统的相关性能参数指标，包括当前预计和当前实际,返回的字典名称为perpar，表示performanceparameters的缩写
    perpar = {}
    p = subprocess.Popen("ulimit -n",shell=True,stdout=subprocess.PIPE)
    perpar['handle'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/tcp_fin_timeout",shell=True,stdout=subprocess.PIPE)
    perpar['timeout_timewait'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/core/wmem_max",shell=True,stdout=subprocess.PIPE)
    perpar['socket_write_buffer'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/core/rmem_max",shell=True,stdout=subprocess.PIPE)
    perpar['socket_read_buffer'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/tcp_syncookies",shell=True,stdout=subprocess.PIPE)
    perpar['syncookies'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/tcp_tw_reuse",shell=True,stdout=subprocess.PIPE)
    perpar['tcpreuse'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/tcp_tw_recycle",shell=True,stdout=subprocess.PIPE)
    perpar['tcprecycle'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/tcp_max_syn_backlog",shell=True,stdout=subprocess.PIPE)
    perpar['tcpsynbacklog'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/tcp_max_tw_buckets",shell=True,stdout=subprocess.PIPE)
    perpar['tcptimemaxbuckets'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/tcp_keepalive_time",shell=True,stdout=subprocess.PIPE)
    perpar['tcpkeepalivetime'] = p.stdout.readlines()[0].strip()
    p = subprocess.Popen("cat /proc/sys/net/ipv4/ip_local_port_range",shell=True,stdout=subprocess.PIPE)
    perpar['iplocalportange'] = p.stdout.readlines()[0].strip().split("\t")
    
    
    return perpar

    


print getNowTime()

serverinfo = PSU()
cpuinfo = serverinfo.getCpuStatus()
meminfo = serverinfo.getMemStatus()
diskinfo = serverinfo.getDiskStatus()

print cpuinfo
print meminfo
print diskinfo
print getSystemInfo()
print getSystemLoad()
print getPerformanceParameters()
