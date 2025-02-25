/*******************************************************************************
 * Copyright (c) 2012, 2014 IBM Corporation.
 *
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v. 1.0 which accompanies this distribution.
 *  
 * The Eclipse Public License is available at http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at
 * http://www.eclipse.org/org/documents/edl-v10.php.
 *
 * Contributors:
 *
 *     Michael Fiedler     - initial API and implementation for Bugzilla adapter
 *     
 * Modifications performed by:    
 *     Axel Reichwein		- implementation for MagicDraw adapter
 *     (axel.reichwein@koneksys.com)
 *     Sebastian Herzig (sebastian.herzig@me.gatech.edu) - support for publishing OSLC resource shapes     
 *******************************************************************************/
package magicdraw;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.Timer;
import java.util.TimerTask;

import org.eclipse.lyo.oslc4j.core.exception.OslcCoreApplicationException;
import org.eclipse.lyo.oslc4j.core.model.AllowedValues;
import org.eclipse.lyo.oslc4j.core.model.Compact;
import org.eclipse.lyo.oslc4j.core.model.CreationFactory;
import org.eclipse.lyo.oslc4j.core.model.Dialog;
import org.eclipse.lyo.oslc4j.core.model.Error;
import org.eclipse.lyo.oslc4j.core.model.ExtendedError;
import org.eclipse.lyo.oslc4j.core.model.Link;
import org.eclipse.lyo.oslc4j.core.model.OAuthConfiguration;
import org.eclipse.lyo.oslc4j.core.model.OslcConstants;
import org.eclipse.lyo.oslc4j.core.model.PrefixDefinition;
import org.eclipse.lyo.oslc4j.core.model.Preview;
import org.eclipse.lyo.oslc4j.core.model.Property;
import org.eclipse.lyo.oslc4j.core.model.Publisher;
import org.eclipse.lyo.oslc4j.core.model.QueryCapability;
import org.eclipse.lyo.oslc4j.core.model.ResourceShape;
import org.eclipse.lyo.oslc4j.core.model.Service;
import org.eclipse.lyo.oslc4j.core.model.ServiceProvider;
import org.eclipse.lyo.oslc4j.core.model.ServiceProviderCatalog;
//import org.eclipse.lyo.oslc4j.provider.jena.JenaProvidersRegistry;
//import org.eclipse.lyo.oslc4j.provider.json4j.Json4JProvidersRegistry;

import edu.gatech.mbsec.adapter.magicdraw.resources.Constants;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLAssociationBlock;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLBlock;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLBlockDiagram;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLConnector;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLConnectorEnd;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLFlowProperty;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLFullPort;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLInterfaceBlock;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLInternalBlockDiagram;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLItemFlow;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLModel;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLPackage;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLPartProperty;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLPort;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLProxyPort;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLReferenceProperty;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLRequirement;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLValueProperty;
import edu.gatech.mbsec.adapter.magicdraw.resources.SysMLValueType;
import magicdraw.MagicDrawManager;


//import com.nomagic.magicdraw.commandline.CommandLine;

/**
 * OSLC4JMagicDrawApplication registers all entity providers for converting
 * POJOs into RDF/XML, JSON and other formats. OSLC4JMagicDrawApplication
 * registers also registers each servlet class containing the implementation of
 * OSLC RESTful web services.
 * 
 * OSLC4JMagicDrawApplication also reads the user-defined configuration file
 * with loadPropertiesFile(). This is done at the initialization of the web
 * application, for example when the first resource or service of the OSLC
 * MagicDraw adapter is requested.
 * 
 * @author Axel Reichwein (axel.reichwein@koneksys.com)
 * @author Sebastian Herzig (sebastian.herzig@me.gatech.edu)
 */

public class Configuration {

	private static final Set<Class<?>> RESOURCE_CLASSES = new HashSet<Class<?>>();
	public static final Map<String, Class<?>> RESOURCE_SHAPE_PATH_TO_RESOURCE_CLASS_MAP = new HashMap<String, Class<?>>();

	
	public static String magicdrawModelsDirectory = null;
	public static String portNumber = null;
	
	public static String projectPath = "C:\\Users\\Sergio\\Downloads\\SysML2Requirements";
	

//	public static String warConfigFilePath = "../oslc4jmagicdraw configuration/config.properties";
//	public static String localConfigFilePath = "oslc4jmagicdraw configuration/config.properties";
	public static String localConfigFilePath = projectPath + "\\Sysml2Requirements\\configuration\\config.properties";
	
	public static String configFilePath = null;
	public static int delayInSecondsBetweenDataRefresh = 100000;
	
	
	
	

	// public static String configFilePath = "configuration/config.properties";

	public static void readDataFromCameoFiles() {
		loadPropertiesFile();
		


		//readDataFirstTime();
		//
		
		reloadModels();

		// readDataPeriodically();
	}

	protected static Properties loadPropertiesFile() {
		Properties prop = new Properties();
		InputStream input = null;
		
			try {
				input = new FileInputStream(localConfigFilePath);
				configFilePath = localConfigFilePath;
			} catch (FileNotFoundException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			} // for war file
		
		// load property file content and convert backslashes into forward
		// slashes
		String str;
		if (input != null) {
			try {
				str = readFile(configFilePath, Charset.defaultCharset());
				prop.load(new StringReader(str.replace("\\", "/")));

				// get the property value
				
				String magicdrawModelsDirectoryFromUser = prop.getProperty("magicdrawModelsDirectory");
				
				String delayInSecondsBetweenDataRefreshFromUser = "none";
				

				// add trailing slash if missing
				if (!magicdrawModelsDirectoryFromUser.endsWith("/")) {
					magicdrawModelsDirectoryFromUser = magicdrawModelsDirectoryFromUser + "/";
				}
				magicdrawModelsDirectory = magicdrawModelsDirectoryFromUser;
				
				portNumber = "8080";
	
				try {
					delayInSecondsBetweenDataRefresh = Integer.parseInt(delayInSecondsBetweenDataRefreshFromUser);
				} catch (Exception e) {

				}

			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} finally {
				try {					
					input.close();
					return prop;
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return null;
	}

	static String readFile(String path, Charset encoding) throws IOException {
		byte[] encoded = Files.readAllBytes(Paths.get(path));
		return encoding.decode(ByteBuffer.wrap(encoded)).toString();
	}

	

	
	public static void readDataFirstTime() {
		Thread thread = new Thread() {
			public void start() {
				
				reloadModels();
			}

		};
		thread.start();
		try {
			thread.join();
			
			// print sysml data to temporary file
			//MagicDrawManager.printSysMLData();
			
			System.out.println("MagicDraw files read and SysML data exported to temporary file");
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void readDataPeriodically() {
		Timer timer = new Timer();
		timer.scheduleAtFixedRate(new TimerTask() {
			public void run() {
				reloadModels();								
			}
		}, delayInSecondsBetweenDataRefresh * 1000, delayInSecondsBetweenDataRefresh * 1000);
	}

	protected static void reloadModels() {
				
		MagicDrawManager.areSysMLProjectsLoaded = false; // to reload MagicDraw	models
		MagicDrawManager.loadSysMLProjects();	
		
	}
	
	
}
