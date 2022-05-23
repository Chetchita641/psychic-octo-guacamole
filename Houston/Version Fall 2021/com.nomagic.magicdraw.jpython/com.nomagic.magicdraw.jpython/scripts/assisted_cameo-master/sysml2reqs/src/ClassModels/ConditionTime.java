package ClassModels;

import java.util.List;

public class ConditionTime {
	
	private List<String> signaturesList;
	private String minTime;
	private String maxTime;
	
	public List<String> getSignaturesList() {
		return signaturesList;
	}
	public void setSignaturesList(List<String> signaturesList) {
		this.signaturesList = signaturesList;
	}
	public String getMinTime() {
		return minTime;
	}
	public void setMinTime(String minTime) {
		this.minTime = minTime;
	}
	public String getMaxTime() {
		return maxTime;
	}
	public void setMaxTime(String maxTime) {
		this.maxTime = maxTime;
	}
	
	

}
