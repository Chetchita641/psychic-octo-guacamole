package ClassModels;

import java.util.List;

public class MDInterface {

	private String interfaceName;
	private List<ValueProperty> interfaceValues;
	
	public String getInterfaceName() {
		return interfaceName;
	}
	public void setInterfaceName(String interfaceName) {
		this.interfaceName = interfaceName;
	}
	public List<ValueProperty> getInterfaceValues() {
		return interfaceValues;
	}
	public void setInterfaceValues(List<ValueProperty> interfaceValues) {
		this.interfaceValues = interfaceValues;
	}
}
