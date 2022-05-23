package ClassModels;

import java.util.List;

import com.nomagic.uml2.ext.magicdraw.interactions.mdfragments.InteractionOperatorKind;

public class IntRequirements {

	private List<ConditionTime> conditionTimes;
	private List<CombFragment> combinedFragment;
	
	public List<ConditionTime> getConditionTimes() {
		return conditionTimes;
	}
	public void setConditionTimes(List<ConditionTime> conditionTimes) {
		this.conditionTimes = conditionTimes;
	}
	public List<CombFragment> getCombinedFragment() {
		return combinedFragment;
	}
	public void setCombinedFragment(List<CombFragment> combinedFragment) {
		this.combinedFragment = combinedFragment;
	}
	
}
