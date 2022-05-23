# Cameo/MagicDraw to Word Document Transformation 

## How SysML2requirements Script Works:
The script is designed to generate plan text tables from a SysML model file.
Primarily, the script reads the model data and creates maps to store its information. After this step, it separates and organizes data correctly in java objects.
Thus, with the organized data, the script creates the tables and correctly writes the data in their rows and columns.
Finally, the script creates a Word format file containing the desired tables.

## Instructions to install Cameo/MagicDraw to Word Document Transformation 

### In the project folder, there is a folder named ReadMe Images containing pictures that should be used in conjunction with this file.
### Pictures will be indicated in the steps below in this setting: **picture x.x**

### 1. Download the Eclipse IDE for Enterprise Java Developers and Configurate the Java Compiler

1. Access the link https://www.eclipse.org/downloads/packages/release/2019-03/r and download the Eclipse IDE for Enterprise Java Developers. 

![Eclipse IDE for Enterprise Java Developers](sysml2reqs/ReadMeImages/2.1-EclipseIDEforEnterpriseJavaDevelopers.png)

2. Export the Eclipse IDE to a folder inside your Local Disk ( Preferably C: ).
3. Please make sure that you have downloaded a Java sdk on your machine. On Windows, you can check under C:\Program Files\Java . 

![Check under the Java Folder](sysml2reqs/ReadMeImages/2.2-CheckundertheJavaFolder.png)

If you don’t yet have a jdk installed, please download it from http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html and install the Jar file. 

![Download jdk 1.8](sysml2reqs/ReadMeImages/2.3-Downloadjdk1.8.png)

4. Make sure that the Java compiler of your Eclipse IDE is a **jdk8** and not a jre (Window -> Preferences... -> Java -> Installed JREs)

![Window->Preferences...->Java->InstalledJREs](sysml2reqs/ReadMeImages/2.4-Window-Preferences...-Java-InstalledJREs.png)

5. If the Java compiler is not JDK8. Click on Add, select Standard VM and click Next, then click on Directory… and select the Java JDK 8 installation directory (not the JRE directory) as your JRE home as displayed in the images.

![Add the jdk8 - Part 1](sysml2reqs/ReadMeImages/2.5-Addthejdk8-Part1.png)
![Add the jdk8 - Part 2](sysml2reqs/ReadMeImages/2.5-Addthejdk8-Part2.png)

6. Mark jdk8 as your installed JRE, and remove the JRE option, and click OK.

![Remove the JRE option](sysml2reqs/ReadMeImages/2.6-RemovetheJREoption.png)

### 2.	Download Cameo Systems Modeler
1.	Download the free **Demo no install version zip file**  *Cameo_Systems_Modeler_Demo_190_sp2_no_install.zip* from

[https://www.magicdraw.com/show_cameo_systems_modeler/download_demo/download_cameo_systems_modeler](https://www.magicdraw.com/show_cameo_systems_modeler/download_demo/download_cameo_systems_modeler "https://www.magicdraw.com/show_cameo_systems_modeler/download_demo/download_cameo_systems_modeler") to install Cameo Systems Modeler v19LTR (sp2)

2.	Unzip file *Cameo_Systems_Modeler_190_sp2_no_install.zip*
**into a directory which has a path with no spaces!**

3.	In the bin directory, specify your system configuration (Java home directory) in the startup script (cam.properties). Default value is `JAVA_HOME=C\:\\Program Files\\Java\\jre1.8.0_201  `

4.	Open Cameo Systems Modeler using *bin/csm.exe* in your Cameo installation directory and create a new random test model just to go through initial dialogs displayed at the first launch of Cameo Systems Modeler (user profile + demo restrictions dialogs)


### 3.	Clone git repository of Sysml2requirements

1. Create a new folder where the project will be saved.
2. Inside this folder, use your Git client to clone the repository using 
   *git clone git@bitbucket.org:koneksys/sysml2requirements.git*


### 4.	Import projects into the Eclipse workspace

1.	In Eclipse, select in the project explorer view File-> Import... -> General -> Existing projects into Workspace, and then select all projects in the *Sysml2Requirements* folder you just cloned.
2.	 Wait for Eclipse to build the workspace. 

![Import projects into the Eclipse workspace](sysml2reqs/ReadMeImages/3-ImportprojectsintotheEclipseworkspace.png)


### 5. Specify the Cameo/MagicDraw installation directory 3 times

1.	In Eclipse, open the Project Explorer view
2.	Expand the *Sysml2Requirements* project
3.	Right click on CAMEO_INSTALL_DIRECTORY and select Properties
4.	Click on Edit next to the location value to specify your local path to your Cameo installation directory

![Specify your local path to your Cameo installation directory in CAMEO_INSTALL_DIRECTORY](sysml2reqs/ReadMeImages/4.4-SpecifyyourlocalpathtoyourCameoinstallationdirectoryinCAMEO_INSTALL_DIRECTORY.png)

5.	After specifying the value, click on *Apply and Close* 
6.	In Eclipse, open the Project Explorer view
7.	Expand the *MagicDraw* project
8.	Right click on MAGIC_DRAW_INSTALL_DIRECTORY and select Properties
9.	Click on Edit next to the location value to specify your local path to your Cameo installation directory

![Specify your local path to your Cameo installation directory in CAMEO_INSTALL_DIRECTORY](sysml2reqs/ReadMeImages/4.9-SpecifyyourlocalpathtoyourCameoinstallationdirectoryinMAGIC_DRAW_INSTALL_DIRECTORY.png)

10. After specifying the value, click on *Apply and Close*
 

### 6. Specify OSGI target platform

In the Package Explorer, expand the MagicDraw project and open target definition file MagicDraw bundles+Running Platform.target. Click Set as Target Platform at the top right in the main editor view.

![Click Set as Target Platform at the top right in the main editor view](sysml2reqs/ReadMeImages/5-ClickSetasTargetPlatformatthetoprightinthemaineditorview.png)


## Instructions to run Cameo/MagicDraw to Word Document Transformation 


### 7.	Specify location of Cameo/MagidDraw models, the name of the Model that will be anayzed and the output directory where the document will be created

Specify the location of the folder containing SysML models which will be considered by the transformation code in the *config.properties* file under *Sysml2Requirements\configuration*.
Note: The file path can contain backslashes. Warning: Do not put quotes around the file path!

1. Specify location of Cameo/MagidDraw models ahead of magicdrawModelsDirectory.
2. Specify the name of the Model that will be anayzed ahead of modelToConvert.
3. Specify the output directory where the document will be created ahead of outputDirectory.

Note: The models and directories names can't have blank spaces.

![Specify location of CameoMagidDraw models, the name of the Model that will be anayzed and the output directory where the document will be created](sysml2reqs/ReadMeImages/6-SpecifylocationofCameoMagidDrawmodels.png)


### 8.	Specify location of Sysml2Requirements directory

1. In the Sysml2Requirements project there is a package named magicdraw. Inside of it there is a class called Configuration.java. Specify the location of the project folder on line 121. `public static String projectPath = "C:\\Users\\Sergio\\Downloads\\SysML2Requirements";`
Note: The right path is the first SysML2Requirements folder. 

![Specify location of Sysml2Requirements directory on line 121](sysml2reqs/ReadMeImages/7-SpecifylocationofSysml2Requirementsdirectory.png)

### 9.	Launching the Cameo/MagicDraw to Word Document transformation

1. In Eclipse, in the Project Explorer view, Select   Run -> Run Configurations... -> in the left view, expand the OSGI Framework -> select the ConvertSysML2WordDoc launch configuration
2. Click on Run

![Launching the CameoMagicDraw to Word Document transformation](sysml2reqs/ReadMeImages/8-LaunchingtheCameoMagicDrawtoWordDocumenttransformation.png)

3. The file with the Requirements tables will be generated in the directory that was written in the config.properties file


Note 1: A message will appear in the Eclipse Console saying that the procedure was successful.

Note 2: After the message in Note 1, it may happen that the software does not finish running after the Word document is generated. In this case, just click on Terminate.
