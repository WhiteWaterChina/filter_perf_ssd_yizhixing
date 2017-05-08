# filter_perf_ssd_yizhixing
    这个工具是基于python的硬盘性能一致性测试工具，分为两部分set_env.sh是安装python和必要的软件包，filter_ssd_perf.py是运行fio并将结果进行处理的部分。
    这个工具是基于rhel和centos上的，7系统OS使用需要安装光盘上的所有包, rpm -ivh *.rpm --nodeps --force.
    先执行sh set_env.sh设置python运行环境；filter_ssd_perf.py会将生成的结果记录到results文件夹中，里面对四个策略都画了一幅图。里面有一致性的计算值、平均值、一致性计算的上下限、
最大值、最小值及坐标。
    默认一致性是按照平均值的±10%计算的，可以修改。
