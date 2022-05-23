
package magicdraw;

import java.io.File;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Properties;

import magicdraw.MagicDrawManager;

import java.io.FileDescriptor;
import java.io.FileOutputStream;
import java.io.PrintStream;

import org.apache.log4j.Logger;


public class ConvertSysML2WordDoc {

final static Logger logger = Logger.getLogger(ConvertSysML2WordDoc.class.getName());
	
	public static void main(String[] args) {
		
		try {			
			magicdraw.Configuration.readDataFromCameoFiles();
			System.setOut(new PrintStream(new FileOutputStream(FileDescriptor.out)));
			
			magicdraw.MapConfiguration.main(args);
			
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 				
	}		
		/**
	     * Returns the value of the passed property
	     *
	     * @param target The property whose value you wish to inspect
	     * @return
	     */	 
}
