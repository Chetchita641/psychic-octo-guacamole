package ClassModels;

import java.util.List;

public class Signal {
	
	private String signalName;
	private List<signalProperties> signalList ;
	
	public String getSignalName() {
		return signalName;
	}
	public void setSignalName(String signalName) {
		this.signalName = signalName;
	}
	public List<signalProperties> getSignalList() {
		return signalList;
	}
	public void setSignalList(List<signalProperties> signalList) {
		this.signalList = signalList;
	}

}
