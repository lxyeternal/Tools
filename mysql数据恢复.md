<center > MYSQL数据库表恢复</center>
author：Blue</br> 
time：2020-08-07 

# 一、背景
1. 备份原因  
mysql是一种关系型数据库，在当前的开发应用中非常广泛。但是在开发的过程中，经常会发生各种各样的意外，导致数据库服务奔溃，数据丢失以及无法启动等事故。本人是由于在python代码在访问数据库的时候，电脑忽然没电，关机导致数据库服务无法重新启动，所以尝试了数据恢复，并成功会付出所有的表。
2. 恢复条件
mysql服务奔溃，数据库数据文件保留  
以macbook为例：`/usr/local/mysql`路径下的`data`文件夹存在  
`.frm`和`.ibd`文件存在
3. 环境要求  
数据库版本：MySQL-5.7.23(没试过其他版本的，应该5.7都是可以的)  
数据库要求：innodb_file_per_table=1
4. 文件说明  
* Innodb 引擎:  
    > xxx.ibd 数据和索引文件  
    > xxx.frm 表结构文件  
* Myisam 引擎: 
    > xxx.frm 表结构文件  
    > xxx.MYD 数据文件  
    > xxx.MYI 索引文件  

# 二、数据恢复步骤
1. 重装数据库  
需要注意的在重装数据库之前先对`/usr/local/mysql/data`文件夹进行备份，可以拷贝出来  
![截屏2020-08-08 上午12.13.01.png](https://i.loli.net/2020/08/08/AqnaxkUC1QdMrv3.png)
重新安装mysql数据库（步骤省略）
2. 新建一个数据库  
新建一个数据库，这里和以前的数据库同不同名都是可以的  
`create database db`
3. 新建表   
**假设要恢复的表名为：`ability`**
-  新建表的结构必须和要恢复的表的结构是**一样**
    
- #### 如果忘记了表的结构，首先就需要找到表结构  
  在数据库中创建一张表名与被恢复表表名一致的表，表结构不限制   
这里以`ability`表为例：  
`create table ability(id int);`  
使用被恢复的`ability.frm`文件替换新创建的同名表的`ability.frm`文件  
注意`ability.frm`文件在`/usr/local/mysql/data/db`路径下  
这里需要注意的是，由于权限的限制无法进行拷贝，所以这里首先设置dat文件夹的权限 
`sudo chmod -R 777 db`  
下图为已替换
![截屏2020-08-08 上午12.43.47.png](https://i.loli.net/2020/08/08/5gZAiI1c2PYw6y3.png)
在数据库中执行` show create table` 语句  
注意需要在show create table查看表结构之前执行` flush tables` 语句，因为如果`ability`表之前被打开过，那么表结构会被缓存在内存中，`show create table`不会报错，也就无法从错误日志中拿到我们需要的信息。   
具体命令如下：   
` flush tables;`   
` show create table ability;` 
![截屏2020-08-09 上午10.35.55.png](https://i.loli.net/2020/08/09/mz1prSqW6QFLlKA.png)
可以发现这里出现了报错，接下来我们就去查看`log_error`,找到表的字段数。  
mac 查看日志路径的sql命令：  
` show variables like 'log_%';` 
![截屏2020-08-09 上午10.36.02.png](https://i.loli.net/2020/08/09/lbJkipHOU1IMLAV.png)
找到日志文件，然后搜索表名就可以找到报错信息：  
![截屏2020-08-09 上午10.36.21.png](https://i.loli.net/2020/08/09/Kwf6aBpu8jDAEkr.png)
可以看到报错提示该表有`4 columns`  
接下来我们删除ability表，重新新建一个4字段的ability表,字段名以及字段类型不限制。  
`  create table ability(id int,id1 int,id2 int,id3 int);`   
再次使用被恢复的` .frm` 文件替换新创建的同名表的` .frm` 文件:  
在MySQL配置文件中添加`innodb_force_recovery=4`，并重启数据库.  
然后执行：` show create table ability;` 得到` ability` 表结构信息。
![截屏2020-08-09 上午11.37.28.png](https://i.loli.net/2020/08/09/UTMozGEAcCkRpyZ.png)
这样我们就找到表的结构了。

4. 表恢复  
这里已经知道了表的结构了，就按照原表的结构新建一张表。  
        ```
        create table ability
            (id int not null auto_increment,  
            username varchar(255),  
            forum varchar(255),
            content_value varchar(100),
            primary key(id)) 
        ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
        ```  

* 将原先的.ibd文件与原先的.frm文件解除绑定

  `alter table ability discard tablespace;`

* 停掉服务，新的`.ibd`文件覆盖旧的`.ibd`文件，再开启服务

* 将新的`.ibd`文件与`.frm`文件进行关联

  `alter table ability import tablespace;`    
    正常情况下不会报错，但是如果报这个
    > Schema mismatch (Table has ROW_TYPE_COMPACT row format, .ibd file has ROW_TYPE_DYNAMIC row format
    
    表类型错误，在创建时候 加上这个  `ROW_FORMAT=DYNAMIC`;   
    或者 `alter table tb_name row_format=DYNAMIC;`   
    然后再执行  `ALTER TABLE tbname IMPORT TABLESPACE; `  




# 三、总结
在本次的数据恢复中，最主要的是表相关的.frm和.ibd文件完整。这样才能恢复出数据。如果忘记了表结构的话，首先就是要通过error_log找到原表结构信息。然后进一步恢复。同时在整个过程中创建的辅助表表名必须和要恢复的表的表名保持一致。

# 参考文章
[1] 数据恢复新姿势——通过ibd和frm文件恢复数据:https://zhuanlan.zhihu.com/p/52185155  
[2] 通过.ibd和.frm恢复mysql数据:https://www.cnblogs.com/meitian/p/9886654.html  
[3] mysql通过ibd恢复数据:https://www.cnblogs.com/jkklearn/p/6654199.html  
[4] mysql通过.ibd和.frm文件恢复数据:https://baishunhua.com/2019/12/17/mysql%E9%80%9A%E8%BF%87-ibd%E5%92%8C-frm%E6%96%87%E4%BB%B6%E6%81%A2%E5%A4%8D%E6%95%B0%E6%8D%AE/
