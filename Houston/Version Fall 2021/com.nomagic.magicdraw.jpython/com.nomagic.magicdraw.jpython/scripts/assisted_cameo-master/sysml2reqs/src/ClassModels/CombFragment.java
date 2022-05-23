package ClassModels;

import java.util.List;

import com.nomagic.uml2.ext.magicdraw.interactions.mdfragments.InteractionOperatorKind;

public class CombFragment {
	
	private InteractionOperatorKind conditionType;
	private String conditionTime;
	private List<String> conditionSignatures;
	
	public InteractionOperatorKind getConditionType() {
		return conditionType;
	}
	public void setConditionType(InteractionOperatorKind conditionType) {
		this.conditionType = conditionType;
	}
	public String getConditionTime() {
		return conditionTime;
	}
	public void setConditionTime(String conditionTime) {
		this.conditionTime = conditionTime;
	}
	public List<String> getConditionSignatures() {
		return conditionSignatures;
	}
	public void setConditionSignatures(List<String> conditionSignatures) {
		this.conditionSignatures = conditionSignatures;
	}
	
	
	
}
