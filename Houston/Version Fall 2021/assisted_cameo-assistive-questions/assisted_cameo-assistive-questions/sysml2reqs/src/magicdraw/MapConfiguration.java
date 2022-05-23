package magicdraw;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import org.apache.poi.xwpf.usermodel.XWPFDocument;
import org.apache.poi.xwpf.usermodel.XWPFParagraph;
import org.apache.poi.xwpf.usermodel.XWPFRun;
import org.apache.poi.xwpf.usermodel.XWPFTable;
import org.apache.poi.xwpf.usermodel.XWPFTableCell;
import org.apache.poi.xwpf.usermodel.XWPFTableRow;
import org.openxmlformats.schemas.wordprocessingml.x2006.main.CTTblWidth;
import org.openxmlformats.schemas.wordprocessingml.x2006.main.STTblWidth;


import com.nomagic.uml2.ext.magicdraw.auxiliaryconstructs.mdinformationflows.InformationFlow;
import com.nomagic.uml2.ext.magicdraw.classes.mddependencies.Dependency;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Classifier;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Element;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.LiteralBoolean;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.LiteralInteger;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.LiteralNull;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.LiteralReal;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.LiteralString;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.NamedElement;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.PackageableElement;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Property;
import com.nomagic.uml2.ext.magicdraw.classes.mdkernel.ValueSpecification;
import com.nomagic.uml2.ext.magicdraw.commonbehaviors.mdsimpletime.Duration;
import com.nomagic.uml2.ext.magicdraw.commonbehaviors.mdsimpletime.DurationConstraint;
import com.nomagic.uml2.ext.magicdraw.commonbehaviors.mdsimpletime.DurationInterval;
import com.nomagic.uml2.ext.magicdraw.compositestructures.mdports.Port;
import com.nomagic.uml2.ext.magicdraw.interactions.mdbasicinteractions.Interaction;
import com.nomagic.uml2.ext.magicdraw.interactions.mdbasicinteractions.Message;
import com.nomagic.uml2.ext.magicdraw.interactions.mdbasicinteractions.MessageOccurrenceSpecification;
import com.nomagic.uml2.ext.magicdraw.interactions.mdfragments.CombinedFragment;
import com.nomagic.uml2.ext.magicdraw.interactions.mdfragments.InteractionConstraint;
import com.nomagic.uml2.ext.magicdraw.interactions.mdfragments.InteractionOperatorKind;
import com.nomagic.uml2.ext.magicdraw.statemachines.mdbehaviorstatemachines.Region;
import com.nomagic.uml2.ext.magicdraw.statemachines.mdbehaviorstatemachines.State;
import com.nomagic.uml2.ext.magicdraw.statemachines.mdbehaviorstatemachines.Transition;

import ClassModels.CombFragment;
import ClassModels.ConditionTime;
import ClassModels.IntRequirements;
import ClassModels.MDInterface;
import ClassModels.ModesRegion;
import ClassModels.PCflow;
import ClassModels.RegionRelation;
import ClassModels.Signal;
import ClassModels.ValueProperty;
import ClassModels.signalProperties;

public class MapConfiguration {

	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub

		Map<String, Collection<com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package>> PrintPackages = magicdraw.MagicDrawManager.projectIdMDSysmlPackagesMap;
				
		Properties prop = Configuration.loadPropertiesFile();
		
		String outputDirectory = prop.getProperty("outputDirectory");
		// add trailing slash if missing
		if (!outputDirectory.endsWith("/")) {
			outputDirectory = outputDirectory + "/";
		}
		
		String modelName = prop.getProperty("modelToConvert");
		
		ModesRegion newMode = IdentifyStates(PrintPackages,modelName);	
		List<MDInterface> newInter = CreateTableInterfaces(PrintPackages,modelName);
		List<Signal> newSignals = CreateTableSignals(PrintPackages,modelName);
		List<PCflow> newPCflow = CreateTableRequirementsTemplate1(PrintPackages,modelName);
		IntRequirements newreq = CreateTableRequirementsTemplate2(PrintPackages,modelName);

		XWPFDocument document = new XWPFDocument();
		
		WriteTableFour(newInter,document);
		
		document.createParagraph().setPageBreak(true);
		
		WriteTableFive(newSignals,document);
		
		document.createParagraph().setPageBreak(true);

		WriteTableSix(newMode,newInter,newSignals,newPCflow,newreq,document);
		
	    FileOutputStream out = new FileOutputStream( new File(outputDirectory + modelName + ".doc"));
	    document.write(out);
	    out.close();
	    document.close();
	    
	    System.out.println("Output document was written successfully");
	}
	
	public static void WriteTableSix(ModesRegion region,List<MDInterface> MDinterList,List<Signal> SignalList, List<PCflow> FlowList, 
									IntRequirements Requirements, XWPFDocument document) {
		int i = 0;
		int j;
		j = WriteTemplateOne(region,MDinterList,SignalList,FlowList,document, i);
		
		i=j;
		j = WriteTemplateThree(FlowList,MDinterList,Requirements,document, i);
		
		i=j;
		WriteTemplateTwo(FlowList, Requirements,document, i);
		
	}
	
	public static int WriteTemplateOne(ModesRegion region,List<MDInterface> MDinterList,List<Signal> SignalList,List<PCflow> FlowList, XWPFDocument document, int i) {
		
		String object = "system ";
		String accOrProvide;
		String portInterface;
		int source1 = 0;
		int source2 = 0;
		
		addParagraph(document,"Table 6: Resulting textual requirements");
		
		XWPFTable TableSixHead = document.createTable();
		
		CTTblWidth widthTableSixHead = TableSixHead.getCTTbl().addNewTblPr().addNewTblW();
		widthTableSixHead.setType(STTblWidth.DXA);
		widthTableSixHead.setW(BigInteger.valueOf(9000));		

		XWPFTableRow tableFirstRow = TableSixHead.getRow(0);
		tableFirstRow.getCell(0).setText("ID");
		tableFirstRow.addNewTableCell().setText("Requirement");
		TableSixHead.getRow(0).setHeight(200);
		
			
		XWPFTable TableSixStateLaunch = document.createTable();
		
		CTTblWidth widthTableSixStateLaunch = TableSixHead.getCTTbl().addNewTblPr().addNewTblW();
		widthTableSixStateLaunch.setType(STTblWidth.DXA);
		widthTableSixStateLaunch.setW(BigInteger.valueOf(9000));		
		
		TableSixStateLaunch.getRow(0).getCell(0).setText("Launch");
		TableSixStateLaunch.getRow(0).setHeight(200);
		
		for(PCflow flow: FlowList) {

			if(flow.getConvoyedName().equals("Acceleration")) {
				
				source1 = getSignalIndex(SignalList, flow.getConvoyedName());
				
				int source = getInterfaceIndex(MDinterList, flow.getSourceName());
				if(source <= 0) {
					source2 = getInterfaceIndex(MDinterList, flow.getTargetName());
					accOrProvide = "provide ";
					portInterface = flow.getTargetName();
				}else {
					source2 = source;
					accOrProvide = "accept ";
					portInterface = flow.getSourceName();
				}
				
				XWPFTable TableSixAceleration = document.createTable();
				
				CTTblWidth widthTableSixAceleration = TableSixHead.getCTTbl().addNewTblPr().addNewTblW();
				widthTableSixAceleration.setType(STTblWidth.DXA);
				widthTableSixAceleration.setW(BigInteger.valueOf(9000));
				
				i++;
				XWPFParagraph paragraph = TableSixAceleration.getRow(0).getCell(0).addParagraph();
				XWPFRun run = paragraph.createRun();
				run.setText("R"+i);
//				run.setVerticalAlignment("baseline");
				TableSixAceleration.getRow(0).addNewTableCell();
				
				paragraph = TableSixAceleration.getRow(0).getCell(1).addParagraph();
				run = paragraph.createRun();
				run.setText("The " + object + "shall " + accOrProvide + flow.getConvoyedName() + " according to " + portInterface + ".");
				run.addBreak();
				run.setText("Note 1: " + flow.getConvoyedName() + " is defined in Table " + "S" + source1 + ".");
				run.addBreak();
				run.setText("Note 2: " + portInterface + " is defined in Table " + "E" + source2 + ".");
//				run.setVerticalAlignment("baseline");
			}
		}
		
		XWPFTable TableSixStateNomOperations = document.createTable();
		
		CTTblWidth widthTableSixStateNomOperations = TableSixHead.getCTTbl().addNewTblPr().addNewTblW();
		widthTableSixStateNomOperations.setType(STTblWidth.DXA);
		widthTableSixStateNomOperations.setW(BigInteger.valueOf(9000));
		
		TableSixStateNomOperations.getRow(0).getCell(0).setText("Nominal Operations");
		TableSixStateNomOperations.getRow(0).setHeight(200);
		for(PCflow flow: FlowList) {
			
			if(flow.getConvoyedName().equals("Acceleration")) {
				
			}else {
				
				source1 = getSignalIndex(SignalList, flow.getConvoyedName());
				
				int source = getInterfaceIndex(MDinterList, flow.getSourceName());
				if(source <= 0) {
					source2 = getInterfaceIndex(MDinterList, flow.getTargetName());
					accOrProvide = "provide ";
					portInterface = flow.getTargetName();
				}else {
					source2 = source;
					accOrProvide = "accept ";
					portInterface = flow.getSourceName();
				}
								
				XWPFTable TableSixNonAceleration = document.createTable();
				
				CTTblWidth widthTableSixNonAceleration = TableSixHead.getCTTbl().addNewTblPr().addNewTblW();
				widthTableSixNonAceleration.setType(STTblWidth.DXA);
				widthTableSixNonAceleration.setW(BigInteger.valueOf(9000));
		        
				i++;
				
				XWPFParagraph paragraph = TableSixNonAceleration.getRow(0).getCell(0).addParagraph();
				XWPFRun run = paragraph.createRun();
				run.setText("R"+i);
//				run.setVerticalAlignment("baseline");
				TableSixNonAceleration.getRow(0).addNewTableCell();

				paragraph = TableSixNonAceleration.getRow(0).getCell(1).addParagraph();
				run = paragraph.createRun();
				run.setText("The " + object + "shall " + accOrProvide + flow.getConvoyedName() + " according to " + portInterface + ".");
				run.addBreak();
				run.setText("Note 1: " + flow.getConvoyedName() + " is defined in Table " + "S" + source1 + ".");
				run.addBreak();
				run.setText("Note 2: " + portInterface + " is defined in Table " + "E" + source2 + ".");
//				run.setVerticalAlignment("baseline");
			}
		}		
		return i;
	}
	
	public static void WriteTemplateTwo(List<PCflow> FlowList, IntRequirements Requirements, XWPFDocument document, int i) {
		
		String object = "system ";
		String diagramElement;
		String condition;
		String elements = null;
		
		for(CombFragment combFragment: Requirements.getCombinedFragment()) {
			
			if(combFragment.getConditionType().toString().equals("loop")) {
				
				condition = combFragment.getConditionTime();
				
				if(combFragment.getConditionSignatures().toString().equals("[]")) {
					
					elements = "<all actions> ";
				}else {
					elements = CreateStringSignals(combFragment.getConditionSignatures());
				}
				
				XWPFTable TableSixTemp2 = document.createTable();
				
				CTTblWidth widthTableSixTemp2 = TableSixTemp2.getCTTbl().addNewTblPr().addNewTblW();
				widthTableSixTemp2.setType(STTblWidth.DXA);
				widthTableSixTemp2.setW(BigInteger.valueOf(9000));
				i++;
				TableSixTemp2.getRow(0).getCell(0).setText("R" + i);
				TableSixTemp2.getRow(0).addNewTableCell();
				TableSixTemp2.getRow(0).getCell(1).setText("The " + object + "shall " + elements + condition + ".");
				
			}else if(combFragment.getConditionType().toString().equals("alt")) {

				diagramElement = " when ";
				condition = combFragment.getConditionTime();
				elements = CreateStringSignals(combFragment.getConditionSignatures());
				
				XWPFTable TableSixTemp2 = document.createTable();
				
				CTTblWidth widthTableSixTemp2 = TableSixTemp2.getCTTbl().addNewTblPr().addNewTblW();
				widthTableSixTemp2.setType(STTblWidth.DXA);
				widthTableSixTemp2.setW(BigInteger.valueOf(9000));
				i++;
				TableSixTemp2.getRow(0).getCell(0).setText("R" + i);
				TableSixTemp2.getRow(0).addNewTableCell();
				TableSixTemp2.getRow(0).getCell(1).setText("The " + object + "shall " + elements + diagramElement + condition + ".");
				
			}else if(combFragment.getConditionType().toString().equals("par")) {

				diagramElement = " while ";				
				String acceptingPar = CreateStringSignalsAcceptingPar(FlowList, combFragment.getConditionSignatures());
				String providingPar = CreateStringSignalsProvidingPar(FlowList, combFragment.getConditionSignatures());
				
				XWPFTable TableSixTemp2 = document.createTable();
				
				CTTblWidth widthTableSixTemp2 = TableSixTemp2.getCTTbl().addNewTblPr().addNewTblW();
				widthTableSixTemp2.setType(STTblWidth.DXA);
				widthTableSixTemp2.setW(BigInteger.valueOf(9000));
				i++;
				TableSixTemp2.getRow(0).getCell(0).setText("R" + i);
				TableSixTemp2.getRow(0).addNewTableCell();
				TableSixTemp2.getRow(0).getCell(1).setText("The " + object + "shall accept " + acceptingPar + diagramElement + "providing " + providingPar + ".");
			}
		}
	}

	public static int WriteTemplateThree(List<PCflow> FlowList,List<MDInterface> MDinterList,IntRequirements Requirements, XWPFDocument document, int i) {
		
		String object = "system ";
		String accOrProvide = null;
		String timeDependency = null;
		List<String> actions = new ArrayList();
		
		for(ConditionTime conditionTime: Requirements.getConditionTimes()) {
			
			timeDependency = conditionTime.getMaxTime();

			for(String action: conditionTime.getSignaturesList()) {
				
				for(PCflow flow: FlowList) {
										
					if(flow.getConvoyedName().equals(action)) {
						
						actions.add(flow.getConvoyedName());
						int source = getInterfaceIndex(MDinterList, flow.getSourceName());
						if(source > 0) {
							accOrProvide = "provide";
						}else {
							accOrProvide = "accept";
						}
					}
				}
			}			
			
			XWPFTable TableSixTemp3 = document.createTable();

			CTTblWidth widthTableSixTemp3 = TableSixTemp3.getCTTbl().addNewTblPr().addNewTblW();
			widthTableSixTemp3.setType(STTblWidth.DXA);
			widthTableSixTemp3.setW(BigInteger.valueOf(9000));
			i++;
			TableSixTemp3.getRow(0).getCell(0).setText("R" + i);
			TableSixTemp3.getRow(0).addNewTableCell();
			TableSixTemp3.getRow(0).getCell(1).setText("The " + object + "shall " + accOrProvide + " " + actions.get(1) + " in less than " 
					+ timeDependency + "s after having reveived " + actions.get(0) + ".");						
		}	
		return i;
	}
	
	public static void WriteTableFour(List<MDInterface> MDinterList, XWPFDocument document) {
	
		addParagraph(document,"Table 4: List of physical interfaces of required properties");
		
		XWPFTable tableFour = document.createTable();	
		
		CTTblWidth widthtableFour = tableFour.getCTTbl().addNewTblPr().addNewTblW();
		widthtableFour.setType(STTblWidth.DXA);
		widthtableFour.setW(BigInteger.valueOf(7000));
		
		XWPFTableRow tableFirstRow = tableFour.getRow(0);

		tableFirstRow.getCell(0).setText("Property");
		tableFirstRow.addNewTableCell().setText("Value");
		tableFirstRow.getCell(0).setVerticalAlignment(XWPFTableCell.XWPFVertAlign.CENTER);
		tableFirstRow.getCell(1).setVerticalAlignment(XWPFTableCell.XWPFVertAlign.CENTER);

		int i = 1;
		
		for(MDInterface mdInterface: MDinterList) {	
			
//			int indexName = mdInterface.getInterfaceName().indexOf("F");	
//			if(indexName >= 0) {
				
				XWPFTableRow tableInterfacesRow = tableFour.createRow();
				
				tableInterfacesRow.getCell(0).setText("E" + (i) +  ": " + mdInterface.getInterfaceName());
				i++;
				
				for(ValueProperty tableText: mdInterface.getInterfaceValues()) {
					
					XWPFTableRow tablePropertiesRow = tableFour.createRow();
					tablePropertiesRow.getCell(0).setText(tableText.getType());
					tablePropertiesRow.getCell(1).setText(tableText.getValue());
//				}
			}
		}
	}
	
	public static void WriteTableFive(List<Signal> SignalList, XWPFDocument document) {
		
		addParagraph(document,"Table 5: Required characteristics of inputs and outputs");

		XWPFTable tableFive = document.createTable();	
		
		CTTblWidth widthtableFive = tableFive.getCTTbl().addNewTblPr().addNewTblW();
		widthtableFive.setType(STTblWidth.DXA);
		widthtableFive.setW(BigInteger.valueOf(7000));
		
		XWPFTableRow tableFirstRow = tableFive.getRow(0);
		
		tableFirstRow.getCell(0).setText("Property");
		tableFirstRow.addNewTableCell().setText("Value");
		tableFirstRow.getCell(0).setVerticalAlignment(XWPFTableCell.XWPFVertAlign.CENTER);
		tableFirstRow.getCell(1).setVerticalAlignment(XWPFTableCell.XWPFVertAlign.CENTER);
		
		int i = 1;
		
		for(Signal signal: SignalList) {
			
			XWPFTableRow tableSignalsRow = tableFive.createRow();
			tableSignalsRow.getCell(0).setText("S" + (i) +  ": " + signal.getSignalName());
			
			i++;
			
			for(signalProperties tableText: signal.getSignalList()) {
				
				XWPFTableRow tablePropertiesRow = tableFive.createRow();
				tablePropertiesRow.getCell(0).setText(tableText.getType());
				tablePropertiesRow.getCell(1).setText(tableText.getValue());
			}
		}
	}
	
	public static ModesRegion IdentifyStates(Map<String, Collection<com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package>> PrintPackages,String packageName) {
		
		ModesRegion modesRegion = new ModesRegion();
		modesRegion.setRegionRelation(new ArrayList());
		modesRegion.setRegionState(new ArrayList());
		
		for(com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package c: PrintPackages.get(packageName)) {
	
			if(c.getName().equals("Modes")) {
			
				for (PackageableElement e : c.getPackagedElement()){
				
					if(e.getHumanType().equals("State Machine")) {
					
						for(Element x: e.getOwnedElement()) {
						
							if(x instanceof Region) {

								for(Transition m: ((Region) x).getTransition()) {
									
									RegionRelation regionRelation = new RegionRelation();
									regionRelation.setRelationSource(m.getSource().getName());
									regionRelation.setRelationTarget(m.getTarget().getName());
									
									modesRegion.getRegionRelation().add(regionRelation);
								}
									
								for(Element w: x.getOwnedElement()) {
								
									if(w instanceof State) {
										
										modesRegion.getRegionState().add(w.getHumanName());
																					
										List<String> clientList = new ArrayList();
											
										for(Dependency q: ((State) w).getSupplierDependency()) {
													
											for(NamedElement z: q.getClient()) {
												
												//Inside Launch and Nominal Operations
												//Dependencies to catch the SysML Diagram Name
											}
										}
									}	
								}									
							}
						}												
					}		
				}
			}
		}
		
		return modesRegion;
	}
	
	public static List<MDInterface> CreateTableInterfaces(Map<String, Collection<com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package>> PrintPackages,String packageName) {
		
		List<MDInterface> interList = new ArrayList();
				
		for(com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package d: PrintPackages.get(packageName)) {	
			if(d.getName().equals("Interfaces")) {
				
				for (PackageableElement e : d.getPackagedElement()){
					
					if(!e.getName().isEmpty()) {
						
						MDInterface inter = new MDInterface();
						inter.setInterfaceValues(new ArrayList());
						
						inter.setInterfaceName(e.getName());
						
						for(Element x: e.getOwnedElement()) {
							
							ValueProperty valPro = new ValueProperty();
							String type = null;
							
							if(x instanceof NamedElement) {
								type = ((NamedElement) x).getName();
							}
				    		valPro.setType(type);
							
							for(Element y: x.getOwnedElement()) {
								
								String value = null;

								if (y instanceof LiteralBoolean) {
						            value = Boolean.toString(((LiteralBoolean) y).isValue());
						        }
						        else if (y instanceof LiteralInteger) {
						            value = Long.toString(((LiteralInteger) y).getValue());
						        }
						        else if (y instanceof LiteralNull) {
						            value = null;
						        }
						        else if (y instanceof LiteralReal) {
						            value = Double.toString(((LiteralReal) y).getValue());
						        }
						        else if (y instanceof LiteralString) {
						            value = ((LiteralString) y).getValue(); 
						        }
								
						    	if(value != null) {
						    		valPro.setValue(value);
						    		inter.getInterfaceValues().add(valPro);
						    	}
							}
							
							if(x instanceof Port) {
								
								String value = null;
								type = "Proxy Port " + ((Port) x).getName();
								value = ((Port) x).getType().getName();
								valPro.setType(type);
								valPro.setValue(value);
								inter.getInterfaceValues().add(valPro);								
							}
						}
						interList.add(inter);
					}
				}
			}
		}
		return interList;
	}
	
	public static List<Signal> CreateTableSignals(Map<String, Collection<com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package>> PrintPackages,String packageName) {
		
		List<Signal> signalList = new ArrayList();
		
		for (com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package h : PrintPackages.get(packageName)) {
			if (h.getName().equals("Signals")) {

				for (PackageableElement e : h.getPackagedElement()) {
		
					if (!e.getName().isEmpty()) {
						
						Signal signal = new Signal();
						signal.setSignalName(e.getName());
						signal.setSignalList(new ArrayList());
						
						
						for (Element w : e.getOwnedElement()) {
							
							signalProperties sigprop = new signalProperties();
							String value = null;
							String type = null;
							ValueSpecification y = null;
							
							if (w instanceof Property) {
								y = ((Property) w).getDefaultValue();
								type = ((Property) w).getName();
							}

							if (y instanceof LiteralBoolean) {
								value = Boolean.toString(((LiteralBoolean) y).isValue());
							} else if (y instanceof LiteralInteger) {
								value = Long.toString(((LiteralInteger) y).getValue());
							} else if (y instanceof LiteralNull) {
								value = null;
							} else if (y instanceof LiteralReal) {
								value = Double.toString(((LiteralReal) y).getValue());
							} else if (y instanceof LiteralString) {
								value = ((LiteralString) y).getValue();
							}
							
							sigprop.setType(type);
							sigprop.setValue(value);
							
							signal.getSignalList().add(sigprop);
							
						}
						signalList.add(signal);
					}
				}
			}
		}
		return signalList;
	}
	
	public static List<PCflow> CreateTableRequirementsTemplate1(Map<String, Collection<com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package>> PrintPackages,String packageName) {
		
		List<PCflow> PcFlowList = new ArrayList();
		
		for (com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package c : PrintPackages.get(packageName)) {

			if (c.getName().equals("Physical connections")) {

				for (PackageableElement e : c.getPackagedElement()) {

					if (e instanceof InformationFlow) {
						
						PCflow pcflow = new PCflow();
						
						if(e instanceof NamedElement) {
							pcflow.setFlowName(e.getName());
						}

						for (Classifier convoyed : ((InformationFlow) e).getConveyed()) {
							pcflow.setConvoyedName(convoyed.getName());							
						}

						for (NamedElement target : ((InformationFlow) e).getInformationTarget()) {
							pcflow.setTargetName(target.getName());
						}

						for (NamedElement source : ((InformationFlow) e).getInformationSource()) {
							pcflow.setSourceName(source.getName());
						}
						
						PcFlowList.add(pcflow);
					}
				}
			}
		}
		return PcFlowList;
	}

	public static IntRequirements CreateTableRequirementsTemplate2(Map<String, Collection<com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package>> PrintPackages,String packageName) {
		
		IntRequirements intReq = new IntRequirements();
		intReq.setConditionTimes(new ArrayList());
		intReq.setCombinedFragment(new ArrayList());
		
		for(com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package c: PrintPackages.get(packageName)) {
		
			if(c.getName().equals("Sequence Diagrams")) {
				
				for (PackageableElement e : c.getPackagedElement()){
					
					if(e.getName().equals("Requirements")) {
						
						for(Element x: e.getOwnedElement()) {
							
							if(x instanceof Interaction){
								
								ConditionTime conditiontime = new ConditionTime();
								List<String> signatureDurationConstraint = new ArrayList();
																
								for(Element z: x.getOwnedElement()) {
									
									if(z instanceof DurationConstraint) {
		
										DurationInterval interval = ((DurationConstraint) z).getSpecification();
										Duration min = interval.getMin();
										Duration max = interval.getMax();

										
										for(Element minElement: min.getOwnedElement()){
											
											conditiontime.setMinTime(((LiteralString) minElement).getValue());
										}
										
										for(Element maxElement: max.getOwnedElement()){
											
											conditiontime.setMaxTime(((LiteralString) maxElement).getValue());
										}
									
										for(Element p: ((DurationConstraint) z).getConstrainedElement()) {
											
											if(p instanceof Message) {
												
												Message message = (Message) p;
												signatureDurationConstraint.add(message.getSignature().getName());
											}
										}
										conditiontime.setSignaturesList(signatureDurationConstraint);
									}

									if(z instanceof CombinedFragment) {  //LOOP

										InteractionOperatorKind interactionOperator = null;										
										interactionOperator = ((CombinedFragment) z).getInteractionOperator();
										
										for(Element k: z.getOwnedElement()) {
		
											for(Element r: k.getOwnedElement()) {
		
												if(r instanceof InteractionConstraint) {
													
													List<String> conditionSignatures = new ArrayList();
													String conditionTime = null;
													
													InteractionConstraint interactionConstraint = (InteractionConstraint) r;
													
													for(Element s: interactionConstraint.getOwnedElement()) {
														
														conditionTime = ((LiteralString) s).getValue();
													}
													CombFragment combFragment = new CombFragment();
													combFragment.setConditionTime(conditionTime);
													combFragment.setConditionType(interactionOperator);
													combFragment.setConditionSignatures(conditionSignatures);
													intReq.getCombinedFragment().add(combFragment);
												}
												
												if(r instanceof CombinedFragment) {
													
													List<String> conditionSignatures = new ArrayList();
													interactionOperator = null;
													String conditionTime = null;
													
													interactionOperator = ((CombinedFragment) r).getInteractionOperator();
													for(Element d: r.getOwnedElement()) {
														
														for(Element t: d.getOwnedElement()) {
															
															MessageOccurrenceSpecification occu = (MessageOccurrenceSpecification) t;
															Message men = occu.getMessage();
															if(!conditionSignatures.contains(men.getSignature().getName())) {
																
																conditionSignatures.add(men.getSignature().getName());
															}	
														}
													}
													CombFragment combFragment = new CombFragment();
													combFragment.setConditionType(interactionOperator);
													combFragment.setConditionSignatures(conditionSignatures);
													combFragment.setConditionTime(null);
													intReq.getCombinedFragment().add(combFragment);
												}												
											}
										}
									}
								}
								intReq.getConditionTimes().add(conditiontime);
							}
						}
					}
				}
			}
		}
		return intReq;
	}
	
//	public static void CreateSearchTable(Map<String, Collection<com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package>> PrintPackages,String packageName,ModesRegion region) {
//		
//		
//		for(com.nomagic.uml2.ext.magicdraw.classes.mdkernel.Package c: PrintPackages.get(packageName)) {
//		
//			if(c.getName().equals("Sequence Diagrams")) {
//				
//				for (PackageableElement e : c.getPackagedElement()){
//					
//					for(String states: region.getRegionState()){
//						
//						if(e.getName().equals("Mechanical Load")) {
//							
//							for(Element x: e.getOwnedElement()) {
//								
//								for(Element y: x.getOwnedElement()) {
//									
//									if(y instanceof Message) {
//										
//										
//									}
//								}
//							}
//						}
//					}		
//				}
//			}
//		}
//	}

	public static String CreateStringSignals(List<String> conditionSignatures) {
		
		String result = "[";
		int i = conditionSignatures.size();
		
		for(String string: conditionSignatures) {
			i--;
			
			if(i!=0) {				
				result = result + string + ", ";
			}else {
				result = result + string + "]";
			}			
		}
		return result;
	}
	
	public static String CreateStringSignalsAcceptingPar(List<PCflow> FlowList, List<String> conditionSignatures){
		
		List<String> acceptList = new ArrayList();
		String result;
		for(String signature: conditionSignatures) {
			
			for(PCflow flowList: FlowList) {
				
				if(flowList.getConvoyedName().equals(signature)) {
					
					int indexTarget = flowList.getTargetName().indexOf("-");
					
					if(indexTarget >= 0) {						
						acceptList.add(signature);			
					}
				}
			}
		}
		
		result = CreateStringSignals(acceptList);
		return result;
	}
	
	public static String CreateStringSignalsProvidingPar(List<PCflow> FlowList, List<String> conditionSignatures){
		
		List<String> acceptList = new ArrayList();
		String result;
		for(String signature: conditionSignatures) {
			
			for(PCflow flowList: FlowList) {
				
				if(flowList.getConvoyedName().equals(signature)) {
					
					int indexSource = flowList.getSourceName().indexOf("-");
					
					if(indexSource >= 0) {						
						acceptList.add(signature);			
					}
				}
			}
		}
		
		result = CreateStringSignals(acceptList);
		return result;
	}
	
	public static void addParagraph(XWPFDocument document, String text) {

		//Creates the new paragraph
		XWPFParagraph paragraph = document.createParagraph();
		//Adds the run, with is used to add text and text styling
		XWPFRun run = paragraph.createRun();
		run.setText(text);
		//Adds a marging after the paragraph
		paragraph.setSpacingAfter(100);
		
	}
	
	public static int getSignalIndex (List<Signal> SignalList, String signalName) {
		
		int index = 0;
		int counter = 0;
		for(Signal signal: SignalList) {
			
			counter++;
			if(signal.getSignalName().equals(signalName)) {
				
				index = counter;
			}
		}
		return index;
	}
	
	public static int getInterfaceIndex(List<MDInterface> MDinterList, String interfaceName) {
	
		int index = 0;
		int counter = 0;
		for(MDInterface mdInterface: MDinterList) {
			
			counter++;
			if(mdInterface.getInterfaceName().equals(interfaceName)) {
				
				index = counter;
			}
		}
		return index;
	}
}
