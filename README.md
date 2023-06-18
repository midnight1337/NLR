# NLR

### 1. Overview
NLR is a tool I've designed for automating log collection on remote devices via SSH commands on Linux OS servers.
Basically performing stuff like connecting with jump server, then connecting with target device, 
then performing logging, waiting a bit and then finally downloading it with SCP on jump hostname client was done fully manually which is super boring when
you do this at least few times per day. I was kinda sick of it so I wanted to automate this stuff as I knew all of these can be 
done with only few clicks.

This tool provides automated:
- connecting into SSH server
- connecting into PC connected to that server
- running particular logs
- watching real time log data (PID, size, logging time, is that particular PID still alive)
- stoping and downloading these logs from remote PC intoo SSH server
- editing database of your's SSH remote servers


This is a topology of whole steps that tool instructions go through when connecting and performing operations:

![Topology](/Pictures/topology.png)

As you can see first you need to initialise connection with remote server which is jump hostname, to be able to
connect to your target which is physical device connected to that VM with copper cable. After establishing both connections
you can start using this tool.

### 2. Functionality of a tool
- #### 2.1. Main screen

  This is a main screen where you can connect to VM, start and watch logs info

![Main screen](/Pictures/gui_logs.jpg)

- #### 2.2. Virtual machine editor

  Here you can edit, add or remove your VMs from database which is simply a text file stored in tool installation directory 

![VM editor](/Pictures/gui_editor.jpg)

- #### 2.3. About Page

  Nothing interesting here, just quick overview and description 

![ABout Page](/Pictures/gui_about.jpg)

- #### 2.4. Selecting and editing VM

  Actual value is value saved into database, planned value field is editable field that user can specify Virtual Machine loging informations.
  By clicking save, it's saved into database, hence these information from planned value become actual value.

![VM Editor](/Pictures/gui_edit_vm.jpg)

- #### 2.5. Connecting to remote and running simple Tcpdump

  You can see that GUI console displayed successful connection to VM as jump hostname, and then to SMOD as target.
  On terminal in background I'm connected into that target client and you can see that there are no processes assigned with tcpdump

![Tcpdump_1](/Pictures/tcpdump_1.jpg)

  When I start logging, tcpdump process appears on remote, and simultaneously all the necessary log information appears on GUI

![Tcpdump_2](/Pictures/tcpdump_2.jpg)

  When I stop logging by clicking STOP button, it simply kills the process and changes status on GUI with console information.
  Then by clicking download button, the log has been copied with SCP command from target physicall device into VM as jump hostname into NLR directory which is created by tool itself.

![Tcpdump_3](/Pictures/tcpdump_3.jpg)

- #### 2.7 Running two logs simultaneously

![Tcpdump_syslog](/Pictures/tcpdump_syslog.jpg)

  Running two kind of logs doesn't affect usability of the tool because they are run in separate thread, 
  you can see that I've successfully run Tcpdump and Syslog

![Tcpdump_syslog_2](/Pictures/tcpdump_syslog_2.jpg)

  When I stop any of the log by killing it from remote server (not from GUI), int his example Syslog, it show information on GUI console that log has been interupted!
  This is very usable information because we know that PID was killed by someone else.

- #### 2.8 Running many sessions in separate threads

  Very strong feature is that every SSH connection, and hence particular log is running as thread in background,
  so user is able to use multiple VMs at once without affecting each other or making tool unusable.

![Thread session](/Pictures/gui_thread_new_session.jpg)

- #### 2.9 Losing connection with remote

  Another cool feature is that, there is a method as thread which checks every second if connection with remote is still alive. If not, there is Windows toast notifier and GUI console output as
  client has disconnected

![Thread session](/Pictures/sysmodule_reboot.jpg)

### 3. UML of the tool

Diagram of how all the classes and methods and files connect with each other

![UML](/Pictures/UML.png)

### 4. How to use it
Well, you can run it, but you can't use it. This code was published only for review purpose, official version contains some company confidential data (which obviously I can't publish) stored in hashdata.py, which is necessary for proper use of a tool.
So unless you're not my co-worker you can't see how does it work.
Please clone repository with:

```
git clone https://github.com/midnight1337/NLR.git
```

NLR works on PC only with Windows 10 OS. Create venv with requirements installed, then run it in your IDE. Your database and backlog file is saved in Documents directory.

### 5. License
This tool is licensed with GNU General Public License v3.0
